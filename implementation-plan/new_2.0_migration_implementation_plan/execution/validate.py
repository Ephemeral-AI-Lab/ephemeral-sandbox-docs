#!/usr/bin/env python3
"""Fail-closed, dependency-free validator for migration execution artifacts."""

from __future__ import annotations

import argparse
import errno
import fcntl
import hashlib
import json
import os
import re
import resource
import selectors
import shutil
import signal
import stat
import struct
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote


EXECUTION_ROOT = Path(__file__).resolve().parent
PLAN_ROOT = EXECUTION_ROOT.parent
TEMPLATE_ROOT = EXECUTION_ROOT / "packet-template"
HISTORY_ROOT = EXECUTION_ROOT / "history"

VERIFIER_MAX_BYTES = 64 * 1024 * 1024
VERIFIER_MAX_ADDRESS_SPACE_BYTES = 256 * 1024 * 1024
VERIFIER_MAX_OPEN_FILES = 32

SCHEMA_NAMES = {
    "gate-catalog.schema.json",
    "execution-state.schema.json",
    "manifest.schema.json",
    "acceptance.schema.json",
    "input-lock.schema.json",
    "phase-entry-attestation.schema.json",
}

SCHEMA_ANNOTATION_KEYS = {"$schema", "$id", "title", "description"}
SCHEMA_SEMANTIC_SHA256 = {
    "acceptance.schema.json": "9bb9d6a85f6b72a926c2d307561c1ae0591aad523b41318463af277668b4cae8",
    "execution-state.schema.json": "2d7193898b531d0f971b3a39fb6a14997dcf344023410cec204394b83658daca",
    "gate-catalog.schema.json": "3c0b1fefc99f7f6bdb2daf62de38ab98b76fe9fb6e3c8c77970f5978b97948ba",
    "input-lock.schema.json": "6fbda4fe90f059514f9e9a74d601d423642dbf6f3e8c6385ab2b17ccb1b314c9",
    "manifest.schema.json": "fe81dcf8beef56879578f37a37885b4fa15af231381628b17d933b30a0299207",
    "phase-entry-attestation.schema.json": "4fa750ea9db0f48f9d1ce8baab2af4996a856e07dfb9445782d8aae0fa93b29e",
}

REQUIRED_PACKET_FILES = {
    "packet.md",
    "manifest.json",
    "acceptance.json",
}

CONTROLLED_PACKET_FILES = REQUIRED_PACKET_FILES - {"manifest.json", "acceptance.json"}

CATALOG_KEYS = {
    "$schema",
    "schema_version",
    "phases",
    "gates",
}

STATE_KEYS = {
    "$schema",
    "schema_version",
    "catalog_sha256",
    "instantiated_gate_count",
    "invalidations",
    "transition",
}

MANIFEST_KEYS = {
    "$schema",
    "schema_version",
    "phase_id",
    "gate_id",
    "lineage_id",
    "packet_maturity",
    "reported_status",
    "report_detail",
    "catalog_sha256",
    "generated_at",
    "source_context",
    "predecessors",
    "input_lock_sha256",
    "producer",
    "artifacts",
    "outputs",
}

ACCEPTANCE_KEYS = {
    "$schema",
    "schema_version",
    "phase_id",
    "gate_id",
    "lineage_id",
    "disposition",
    "disposition_detail",
    "manifest_sha256",
    "accepted_outputs",
    "accepted_by",
    "accepted_at",
}

INVALIDATION_KEYS = {
    "trigger_sha256",
    "recorded_at",
    "affected",
}

ARCHIVE_KEYS = {
    "gate_id",
    "manifest_sha256",
    "acceptance_sha256",
}

PACKET_IDENTITY_KEYS = {
    "gate_id",
    "lineage_id",
    "manifest_sha256",
    "acceptance_sha256",
}

LINEAGE_IDENTITY_KEYS = {
    "gate_id",
    "lineage_id",
}

STATE_TRANSITION_KEYS = {
    "kind",
    "prior_state_sha256",
    "prior_packets",
    "replacement",
    "published_at",
    "published_by",
    "publication",
}

PUBLICATION_KEYS = {
    "method",
    "operation_id",
    "prior_token",
    "lease_id",
    "fencing_token",
    "authority",
}

INPUT_LOCK_KEYS = {
    "$schema",
    "schema_version",
    "phase_id",
    "gate_id",
    "lineage_id",
    "catalog_sha256",
    "locked_at",
    "producer",
    "predecessors",
    "entries",
}

PHASE_ENTRY_ATTESTATION_KEYS = {
    "$schema",
    "schema_version",
    "catalog_sha256",
    "phase_id",
    "gate_id",
    "lineage_id",
    "authorization_receipt_sha256",
    "authorized_actors",
    "authorizer",
    "validity",
}

PRINCIPAL_KEYS = {
    "principal_id",
    "credential_fingerprint",
    "control_domain_fingerprint",
}
ACTION_PRINCIPAL_KEYS = PRINCIPAL_KEYS | {"proof"}
ACTOR_KEYS = PRINCIPAL_KEYS | {"capabilities"}

AUTHORITY_POLICY_KEYS = {"policy_version", "catalog_sha256", "bindings"}
AUTHORITY_BINDING_KEYS = {"key", "use", "verifier"}
AUTHORITY_LOOKUP_KEYS = {
    "kind",
    "phase_id",
    "gate_id",
    "lineage_id",
    "artifact_sha256",
    "bound_sha256",
}
AUTHORITY_VERIFIER_KEYS = PRINCIPAL_KEYS | {
    "executable",
    "build_sha256",
    "trust_root_sha256",
}
AUTHORITY_ARTIFACT_KINDS = {
    "phase-entry-attestation",
    "input-lock",
    "manifest",
    "acceptance",
    "execution-state",
}
AUTHORITY_USES = {
    "CURRENT_AUTHORITY",
    "HISTORICAL_VERIFY_ONLY",
    "ONE_SHOT_STATE_COMMIT",
}

PACKET_SECTION_MARKERS = (
    "<!-- packet:plan -->",
    "<!-- packet:algorithms -->",
    "<!-- packet:evaluation -->",
    "<!-- packet:verification -->",
    "<!-- packet:handoff -->",
    "<!-- packet:end -->",
)

PACKET_SECTION_NAMES = (
    "plan",
    "algorithms",
    "evaluation",
    "verification",
    "handoff",
)

PLAN_SECTION_MARKERS = (
    "<!-- plan:spec -->",
    "<!-- plan:decisions -->",
    "<!-- plan:end -->",
)

PLAN_SPEC_HEADINGS = (
    "## Identity and authority",
    "## Exact consumed inputs",
    "## Objective, non-goals, and success predicate",
    "## Scope and disposition",
    "## Work DAG and safe parallelism",
    "## Resource and safety envelope",
    "## Evidence protocols",
    "## Outputs and handoff",
    "## Invalidation and reopening",
)

PLAN_DECISION_HEADINGS = (
    "## Consumed decisions",
    "## Local decision ledger",
    "## Rejected assumptions",
    "## Downstream impact",
)

EVALUATION_SECTION_MARKERS = (
    "<!-- evaluation:experiments -->",
    "<!-- evaluation:benchmarks -->",
    "<!-- evaluation:end -->",
)

ALGORITHM_SECTION_ANCHORS = (
    "algorithm",
    "inventory",
    "proof",
    "complexity",
    "time",
    "memory",
    "persistent",
    "cleanup",
    "standard",
    "evidence",
    "collision",
)

VERIFICATION_SECTION_ANCHORS = (
    "verification",
    "matrix",
    "predicate",
    "evidence",
    "status",
    "terminal",
    "fault",
    "structural",
    "provenance",
    "verdict",
)

HANDOFF_SECTION_ANCHORS = (
    "handoff",
    "current disposition",
    "read and verify first",
    "next allowed",
    "next forbidden",
    "blockers",
    "invalidation response",
    "manifest",
    "acceptance",
    "lineage",
)

GATE_STATUSES = {"NOT_RUN", "PARTIAL", "PASS", "FAIL", "BLOCKED"}
DIGEST = re.compile(r"^[0-9a-f]{64}$")
ACTION_PROOF = re.compile(r"^[A-Za-z0-9_-]{16,4096}$")
BOUNDED_TOKEN = re.compile(r"^[A-Za-z0-9._:-]{1,256}$")
GIT_OBJECT_ID = re.compile(r"^([0-9a-f]{40}|[0-9a-f]{64})$")
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
LINEAGE = re.compile(r"^[a-z0-9-]+-r\d{4}$")
PHASE_ID = re.compile(r"^[0-9]{2}$")
GATE_ID = re.compile(r"^(?P<phase>[0-9]{2})(?:[a-z])?-[a-z0-9-]+$")
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  (.+)$")
INVALIDATION_RECEIPT_PATH = re.compile(r"^evidence/invalidation-receipts/([0-9a-f]{64})\.json$")
PLACEHOLDER_MARKERS = (
    "[phase-id]",
    "[gate-id]",
    "[replace]",
    "[digest]",
    "[NNNN]",
    "[gate]-",
)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.checks = 0

    def require(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.errors.append(message)

    def finish(self) -> None:
        if self.errors:
            for error in self.errors:
                print(f"ERROR: {error}", file=sys.stderr)
            print(
                f"FAIL execution artifact contract: {len(self.errors)} error(s), "
                f"{self.checks} checks",
                file=sys.stderr,
            )
            raise SystemExit(1)
        print(f"PASS execution artifact contract: {self.checks} checks")


class DuplicateJsonMemberError(ValueError):
    """Raised before semantic validation when a JSON object repeats a name."""


def decode_json(text: str) -> object:
    """Parse one unambiguous JSON value; member names are unique recursively."""

    def unique_object(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for name, member in pairs:
            if name in value:
                raise DuplicateJsonMemberError(f"duplicate object member {name!r}")
            value[name] = member
        return value

    return json.loads(text, object_pairs_hook=unique_object)


def load_json(path: Path, validation: Validation) -> dict:
    try:
        label = path.relative_to(PLAN_ROOT).as_posix()
    except ValueError:
        label = str(path)
    try:
        value = decode_json(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, DuplicateJsonMemberError) as exc:
        validation.require(False, f"cannot parse JSON {label}: {exc}")
        return {}
    validation.require(isinstance(value, dict), f"JSON root must be an object: {label}")
    return value if isinstance(value, dict) else {}


def validate_json_parser_contract(validation: Validation) -> None:
    """Regression-lock the common parser used by every authoritative JSON class."""
    categories = (
        "schema",
        "gate catalog",
        "execution state",
        "packet manifest",
        "acceptance",
        "input lock",
        "phase-entry attestation",
        "external authority policy",
    )
    adversaries = (
        '{"schema_version":1,"schema_version":2}',
        '{"outer":{"decision":"PASS","decision":"FAIL"}}',
    )
    for category in categories:
        for depth, payload in enumerate(adversaries, start=1):
            rejected = False
            try:
                decode_json(payload)
            except DuplicateJsonMemberError:
                rejected = True
            validation.require(
                rejected,
                f"{category} parser accepted duplicate member regression {depth}",
            )


def principal_tuple(value: object) -> tuple[str, str, str] | None:
    """Return the one authenticated security identity used by every role."""
    if not isinstance(value, dict) or not PRINCIPAL_KEYS <= set(value):
        return None
    principal_id = value.get("principal_id")
    credential = value.get("credential_fingerprint")
    control_domain = value.get("control_domain_fingerprint")
    if (
        not isinstance(principal_id, str)
        or not principal_id
        or len(principal_id) > 256
        or not is_digest(credential)
        or not is_digest(control_domain)
    ):
        return None
    return principal_id, str(credential), str(control_domain)


def validate_principal(
    value: object,
    expected_keys: set[str],
    label: str,
    validation: Validation,
) -> tuple[str, str, str] | None:
    validation.require(
        isinstance(value, dict) and set(value) == expected_keys,
        f"{label} field set malformed",
    )
    principal = principal_tuple(value)
    validation.require(principal is not None, f"{label} principal malformed")
    if isinstance(value, dict) and "proof" in expected_keys:
        proof = value.get("proof")
        validation.require(
            isinstance(proof, str) and ACTION_PROOF.fullmatch(proof) is not None,
            f"{label} proof must be bounded unpadded base64url",
        )
    return principal


def principals_are_axis_independent(*principals: tuple[str, str, str] | None) -> bool:
    """Every principal, credential, and control domain must be pairwise distinct."""
    if any(principal is None for principal in principals):
        return False
    concrete = [principal for principal in principals if principal is not None]
    return all(
        len({principal[axis] for principal in concrete}) == len(concrete)
        for axis in range(3)
    )


def authority_lookup_tuple(key: dict) -> tuple[str, str, str, str, str, str]:
    return (
        str(key.get("kind")),
        str(key.get("phase_id")),
        str(key.get("gate_id")),
        str(key.get("lineage_id")),
        str(key.get("artifact_sha256")),
        str(key.get("bound_sha256")),
    )


def phase_capability_contract(
    actors: object,
    phase_gate_ids: list[str],
) -> tuple[set[str], set[str], list[tuple[int, str]]]:
    """Return the required/observed grants and any actor holding both gate sides."""
    required = {
        f"{action}:{gate_id}"
        for gate_id in phase_gate_ids
        for action in ("produce", "accept")
    }
    observed: set[str] = set()
    conflicts: list[tuple[int, str]] = []
    if not isinstance(actors, list):
        return required, observed, conflicts
    for index, actor in enumerate(actors):
        capabilities = actor.get("capabilities") if isinstance(actor, dict) else None
        if not isinstance(capabilities, list):
            continue
        actor_capabilities = {str(capability) for capability in capabilities}
        observed.update(actor_capabilities)
        for gate_id in phase_gate_ids:
            if {f"produce:{gate_id}", f"accept:{gate_id}"} <= actor_capabilities:
                conflicts.append((index, gate_id))
    return required, observed, conflicts


def validate_authority_guard_contract(validation: Validation) -> None:
    """Regression-lock all three identity axes and exact artifact dispatch."""
    actor = ("actor", "a" * 64, "1" * 64)
    acceptor = ("acceptor", "b" * 64, "2" * 64)
    verifier = ("verifier", "c" * 64, "3" * 64)
    validation.require(
        principals_are_axis_independent(actor, acceptor, verifier),
        "authority guard rejected three fully independent principals",
    )
    for axis, label in enumerate(("principal", "credential", "control domain")):
        alias = list(acceptor)
        alias[axis] = actor[axis]
        validation.require(
            not principals_are_axis_independent(actor, tuple(alias), verifier),
            f"authority guard accepted a shared {label}",
        )
    old_key = {
        "kind": "phase-entry-attestation",
        "phase_id": "00",
        "gate_id": "00-evidence-seal",
        "lineage_id": "00-evidence-seal-r0001",
        "artifact_sha256": "d" * 64,
        "bound_sha256": "e" * 64,
    }
    changed_key = dict(old_key, artifact_sha256="f" * 64)
    validation.require(
        authority_lookup_tuple(old_key) != authority_lookup_tuple(changed_key),
        "authority dispatch allowed a historical binding to select new bytes",
    )
    separated_actors = [
        {"capabilities": ["produce:gate-a", "produce:gate-b"]},
        {"capabilities": ["accept:gate-a", "accept:gate-b"]},
    ]
    required, observed, conflicts = phase_capability_contract(
        separated_actors,
        ["gate-a", "gate-b"],
    )
    validation.require(
        required == observed and not conflicts,
        "phase capability guard rejected exhaustive separated grants",
    )
    _, missing_observed, _ = phase_capability_contract(
        [{"capabilities": ["produce:gate-a", "accept:gate-a"]}],
        ["gate-a", "gate-b"],
    )
    validation.require(
        missing_observed != required,
        "phase capability guard accepted an incomplete actor-set union",
    )
    _, _, dual_side_conflicts = phase_capability_contract(
        [{"capabilities": ["accept:gate-a", "produce:gate-a"]}],
        ["gate-a"],
    )
    validation.require(
        dual_side_conflicts == [(0, "gate-a")],
        "phase capability guard accepted one actor on both sides of a gate",
    )
    current_entry = {"archived": False, "phase_id": "01"}
    archived_descendant = {"archived": True, "phase_id": "01"}
    completed_entry = {"archived": False, "phase_id": "00"}
    validation.require(
        authority_record_use(current_entry, "01") == "CURRENT_AUTHORITY",
        "current phase-entry attestation lost current authority",
    )
    validation.require(
        authority_record_use(archived_descendant, "01")
        == "HISTORICAL_VERIFY_ONLY",
        "archived descendant retained current authority",
    )
    validation.require(
        authority_record_use(completed_entry, "01")
        == "HISTORICAL_VERIFY_ONLY",
        "completed phase retained current authority",
    )
    validation.require(
        packet_lifecycle_pair_is_legal("SEALED", "NOT_RUN"),
        "lifecycle guard rejected the authenticated producer-seal interval",
    )
    validation.require(
        not packet_lifecycle_pair_is_legal("INPUT_LOCKED", "PASS"),
        "lifecycle guard accepted a verdict before producer sealing",
    )
    validation.require(
        principals_are_axis_independent(actor, verifier),
        "sealed-without-verdict guard rejected producer/verifier independence",
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        # Every caller also validates the file's existence or compares the
        # result with a required digest.  An unreadable file must therefore
        # become a normal contract failure, never an uncaught validator crash.
        return ""
    return digest.hexdigest()


def open_absolute_nofollow(path: Path, leaf_flags: int = os.O_RDONLY) -> int:
    """Open one absolute lexical path without following any component symlink."""
    if not path.is_absolute():
        raise OSError("path is not absolute")
    components = list(path.parts[1:])
    if not components or any(component in {"", ".", ".."} for component in components):
        raise OSError("path contains an empty, dot, or parent component")
    required = ("O_CLOEXEC", "O_DIRECTORY", "O_NOFOLLOW")
    if any(not hasattr(os, name) for name in required):
        raise OSError("platform lacks no-follow component-open support")
    directory_fd = os.open(
        "/",
        os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC,
    )
    try:
        for component in components[:-1]:
            next_fd = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=directory_fd,
            )
            os.close(directory_fd)
            directory_fd = next_fd
        return os.open(
            components[-1],
            leaf_flags | os.O_NOFOLLOW | os.O_CLOEXEC,
            dir_fd=directory_fd,
        )
    finally:
        os.close(directory_fd)


def stable_stat_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_uid,
        value.st_gid,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def read_stable_regular_fd(fd: int, maximum_bytes: int) -> bytes:
    """Read bounded bytes from one regular open object and detect observed drift."""
    before = os.fstat(fd)
    if not stat.S_ISREG(before.st_mode):
        raise OSError("opened object is not a regular file")
    if before.st_size < 0 or before.st_size > maximum_bytes:
        raise OSError("opened object exceeds its byte bound")
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = os.read(fd, min(1024 * 1024, maximum_bytes + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > maximum_bytes:
            raise OSError("opened object exceeds its byte bound")
    after = os.fstat(fd)
    if stable_stat_identity(before) != stable_stat_identity(after):
        raise OSError("opened object changed while being read")
    return b"".join(chunks)


def validate_native_elf_fd(
    fd: int,
    file_size: int,
    require_self_contained: bool = True,
) -> None:
    """Parse a bounded ELF32/ELF64 image and reject external loader dependencies."""
    identity = os.pread(fd, 16, 0)
    if len(identity) != 16 or identity[:4] != b"\x7fELF":
        raise OSError("verifier must be a native ELF object; scripts are unbound")
    elf_class = identity[4]
    data_encoding = identity[5]
    if elf_class not in {1, 2}:
        raise OSError("verifier ELF class is unsupported")
    if data_encoding not in {1, 2}:
        raise OSError("verifier ELF byte order is unsupported")
    if identity[6] != 1:
        raise OSError("verifier ELF identification version is unsupported")
    byte_order = "<" if data_encoding == 1 else ">"
    if elf_class == 1:
        header_size = 52
        program_header_size = 32
        header_format = byte_order + "HHIIIIIHHHHHH"
        program_header_format = byte_order + "IIIIIIII"
        dynamic_format = byte_order + "iI"
    else:
        header_size = 64
        program_header_size = 56
        header_format = byte_order + "HHIQQQIHHHHHH"
        program_header_format = byte_order + "IIQQQQQQ"
        dynamic_format = byte_order + "qQ"
    header = os.pread(fd, header_size, 0)
    if len(header) != header_size:
        raise OSError("verifier ELF header is truncated")
    fields = struct.unpack(header_format, header[16:])
    elf_type = fields[0]
    elf_version = fields[2]
    program_header_offset = fields[4]
    encoded_header_size = fields[7]
    encoded_program_header_size = fields[8]
    program_header_count = fields[9]
    if elf_type not in {2, 3}:
        raise OSError("verifier ELF is neither executable nor position-independent executable")
    if elf_version != 1:
        raise OSError("verifier ELF version is unsupported")
    if encoded_header_size != header_size:
        raise OSError("verifier ELF header-size declaration is malformed")
    if encoded_program_header_size != program_header_size:
        raise OSError("verifier ELF program-header size is malformed")
    if program_header_count == 0 or program_header_count == 0xFFFF:
        raise OSError("verifier ELF program-header count is unsupported")
    if program_header_count > 4096:
        raise OSError("verifier ELF program-header count exceeds the reviewed bound")
    if program_header_offset < header_size:
        raise OSError("verifier ELF program-header table overlaps its header")
    table_bytes = program_header_count * program_header_size
    if program_header_offset > file_size or table_bytes > file_size - program_header_offset:
        raise OSError("verifier ELF program-header table is outside the object")

    load_segment_seen = False
    dynamic_ranges: list[tuple[int, int]] = []
    for index in range(program_header_count):
        offset = program_header_offset + index * program_header_size
        raw_program_header = os.pread(fd, program_header_size, offset)
        if len(raw_program_header) != program_header_size:
            raise OSError("verifier ELF program-header table changed or truncated")
        program_header = struct.unpack(program_header_format, raw_program_header)
        segment_type = program_header[0]
        if elf_class == 1:
            segment_offset = program_header[1]
            file_bytes = program_header[4]
            memory_bytes = program_header[5]
            alignment = program_header[7]
        else:
            segment_offset = program_header[2]
            file_bytes = program_header[5]
            memory_bytes = program_header[6]
            alignment = program_header[7]
        if file_bytes > 0 and (segment_offset > file_size or file_bytes > file_size - segment_offset):
            raise OSError("verifier ELF segment bytes are outside the object")
        if segment_type == 1:
            load_segment_seen = True
            if file_bytes > memory_bytes:
                raise OSError("verifier ELF load segment has file bytes beyond memory bytes")
        if alignment not in {0, 1} and alignment & (alignment - 1):
            raise OSError("verifier ELF segment alignment is not a power of two")
        if require_self_contained and segment_type == 3:
            raise OSError("verifier ELF declares PT_INTERP; external loader closure is unbound")
        if segment_type == 2 and file_bytes > 0:
            dynamic_ranges.append((segment_offset, file_bytes))
    if not load_segment_seen:
        raise OSError("verifier ELF has no loadable segment")

    if not require_self_contained:
        return
    dynamic_entry_size = struct.calcsize(dynamic_format)
    for dynamic_offset, dynamic_bytes in dynamic_ranges:
        if dynamic_bytes % dynamic_entry_size:
            raise OSError("verifier ELF dynamic table is malformed")
        for offset in range(dynamic_offset, dynamic_offset + dynamic_bytes, dynamic_entry_size):
            raw_dynamic = os.pread(fd, dynamic_entry_size, offset)
            if len(raw_dynamic) != dynamic_entry_size:
                raise OSError("verifier ELF dynamic table changed or truncated")
            tag, _ = struct.unpack(dynamic_format, raw_dynamic)
            if tag == 1:
                raise OSError("verifier ELF declares DT_NEEDED; shared-library closure is unbound")
            if tag == 0:
                break


def validate_executable_stat(before: os.stat_result, maximum_bytes: int) -> None:
    """Reject an executable object outside the reviewed type, mode, or size bound."""
    if not stat.S_ISREG(before.st_mode):
        raise OSError("verifier is not a regular file")
    if before.st_mode & 0o111 == 0:
        raise OSError("verifier has no execute bit")
    if before.st_mode & 0o222:
        raise OSError("verifier object is writable; exact-build custody is not write-denied")
    if before.st_size < 4 or before.st_size > maximum_bytes:
        raise OSError("verifier size is outside the reviewed bound")


def hash_stable_executable_fd(
    fd: int,
    maximum_bytes: int = VERIFIER_MAX_BYTES,
    require_self_contained: bool = True,
) -> str:
    """Hash and structurally bind one retained native verifier descriptor."""
    before = os.fstat(fd)
    validate_executable_stat(before, maximum_bytes)
    os.lseek(fd, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    total = 0
    while True:
        chunk = os.read(fd, min(1024 * 1024, maximum_bytes + 1 - total))
        if not chunk:
            break
        total += len(chunk)
        if total > maximum_bytes:
            raise OSError("verifier exceeds the reviewed byte bound")
        digest.update(chunk)
    validate_native_elf_fd(fd, before.st_size, require_self_contained)
    after = os.fstat(fd)
    if stable_stat_identity(before) != stable_stat_identity(after):
        raise OSError("verifier changed while being hashed or structurally parsed")
    return digest.hexdigest()


def sealed_fd_exec_supported() -> bool:
    required_fcntl_names = {
        "F_ADD_SEALS",
        "F_GET_SEALS",
        "F_SEAL_SEAL",
        "F_SEAL_SHRINK",
        "F_SEAL_GROW",
        "F_SEAL_WRITE",
    }
    return (
        sys.platform.startswith("linux")
        and os.execve in os.supports_fd
        and hasattr(os, "memfd_create")
        and hasattr(os, "MFD_ALLOW_SEALING")
        and hasattr(os, "MFD_CLOEXEC")
        and all(hasattr(fcntl, name) for name in required_fcntl_names)
    )


def verifier_process_limit_is_enforceable() -> bool:
    """Reject privilege states that can bypass the verifier process limit."""
    if not sys.platform.startswith("linux") or not hasattr(os, "getresuid"):
        return False
    if any(uid == 0 for uid in os.getresuid()):
        return False
    capability_names = {"CapInh", "CapPrm", "CapEff", "CapAmb"}
    observed: dict[str, int] = {}
    try:
        for line in Path("/proc/self/status").read_text(encoding="ascii").splitlines():
            name, separator, raw_value = line.partition(":")
            if separator and name in capability_names:
                observed[name] = int(raw_value.strip(), 16)
    except (OSError, UnicodeError, ValueError):
        return False
    return set(observed) == capability_names and all(value == 0 for value in observed.values())


def required_executable_seal_mask() -> int:
    return (
        fcntl.F_SEAL_SEAL
        | fcntl.F_SEAL_SHRINK
        | fcntl.F_SEAL_GROW
        | fcntl.F_SEAL_WRITE
    )


def require_sealed_executable_fd(fd: int) -> None:
    """Prove that one executable descriptor can no longer change size or bytes."""
    if not sealed_fd_exec_supported():
        raise OSError("sealed exact-fd execution is unsupported on this platform")
    validate_executable_stat(os.fstat(fd), VERIFIER_MAX_BYTES)
    if os.get_inheritable(fd):
        raise OSError("verifier clone is not close-on-successful-exec")
    observed = fcntl.fcntl(fd, fcntl.F_GET_SEALS)
    required = required_executable_seal_mask()
    if observed & required != required:
        raise OSError("verifier clone lacks the complete immutable seal set")


def clone_to_sealed_executable_fd(
    source_fd: int,
    maximum_bytes: int = VERIFIER_MAX_BYTES,
) -> int:
    """Copy one bounded source object into a write-sealed anonymous executable."""
    if not sealed_fd_exec_supported():
        raise OSError("sealed exact-fd execution is unsupported on this platform")
    source_before = os.fstat(source_fd)
    validate_executable_stat(source_before, maximum_bytes)
    clone_fd = os.memfd_create(
        "ephemeral-authority-verifier",
        os.MFD_ALLOW_SEALING | os.MFD_CLOEXEC,
    )
    try:
        offset = 0
        while offset < source_before.st_size:
            chunk = os.pread(
                source_fd,
                min(1024 * 1024, source_before.st_size - offset),
                offset,
            )
            if not chunk:
                raise OSError("verifier source truncated while being cloned")
            view = memoryview(chunk)
            while view:
                written = os.write(clone_fd, view)
                if written <= 0:
                    raise OSError("verifier clone write made no progress")
                view = view[written:]
            offset += len(chunk)
        source_after = os.fstat(source_fd)
        if stable_stat_identity(source_before) != stable_stat_identity(source_after):
            raise OSError("verifier source changed while being cloned")
        os.fchmod(clone_fd, 0o555)
        fcntl.fcntl(clone_fd, fcntl.F_ADD_SEALS, required_executable_seal_mask())
        require_sealed_executable_fd(clone_fd)
        os.lseek(clone_fd, 0, os.SEEK_SET)
        return clone_fd
    except BaseException:
        os.close(clone_fd)
        raise


def apply_verifier_resource_limits(timeout_seconds: float) -> None:
    """Bound one trusted verifier child without adding a helper or daemon."""
    cpu_soft = max(1, int(timeout_seconds) + 1)
    requested = (
        (resource.RLIMIT_AS, VERIFIER_MAX_ADDRESS_SPACE_BYTES, VERIFIER_MAX_ADDRESS_SPACE_BYTES),
        (resource.RLIMIT_CPU, cpu_soft, cpu_soft + 1),
        (resource.RLIMIT_CORE, 0, 0),
        (resource.RLIMIT_FSIZE, 0, 0),
        (resource.RLIMIT_NOFILE, VERIFIER_MAX_OPEN_FILES, VERIFIER_MAX_OPEN_FILES),
        (resource.RLIMIT_NPROC, 1, 1),
    )
    for kind, desired_soft, desired_hard in requested:
        _, current_hard = resource.getrlimit(kind)
        bounded_hard = (
            desired_hard
            if current_hard == resource.RLIM_INFINITY
            else min(desired_hard, current_hard)
        )
        resource.setrlimit(kind, (min(desired_soft, bounded_hard), bounded_hard))


def terminate_verifier_process_group(pid: int) -> None:
    """Kill a verifier session, falling back to its leader before setsid."""
    try:
        os.killpg(pid, signal.SIGKILL)
    except OSError:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass


def wait_for_verifier_child(pid: int, options: int = 0) -> tuple[int, int]:
    """Reap the direct verifier child without treating EINTR as completion."""
    while True:
        try:
            return os.waitpid(pid, options)
        except InterruptedError:
            continue


def run_sealed_exact_fd(
    executable_fd: int,
    argv: list[str],
    timeout_seconds: float = 30.0,
    output_limit: int = 64 * 1024,
) -> tuple[int, bytes, bytes, str | None]:
    """Execute one immutable descriptor with bounded output, time, and environment."""
    try:
        require_sealed_executable_fd(executable_fd)
    except OSError as exc:
        return 127, b"", b"", str(exc)
    stdout_read = -1
    stdout_write = -1
    stderr_read = -1
    stderr_write = -1
    pid = -1
    selector: selectors.BaseSelector | None = None
    try:
        stdout_read, stdout_write = os.pipe()
        stderr_read, stderr_write = os.pipe()
        pid = os.fork()
        if pid == 0:
            try:
                os.setsid()
                null_fd = os.open("/dev/null", os.O_RDONLY | os.O_CLOEXEC)
                os.dup2(null_fd, 0)
                os.close(null_fd)
                os.dup2(stdout_write, 1)
                os.dup2(stderr_write, 2)
                for descriptor in (stdout_read, stdout_write, stderr_read, stderr_write):
                    if descriptor not in {1, 2}:
                        os.close(descriptor)
                os.chdir("/")
                os.umask(0o077)
                apply_verifier_resource_limits(timeout_seconds)
                require_sealed_executable_fd(executable_fd)
                os.execve(
                    executable_fd,
                    argv,
                    {"LC_ALL": "C", "TZ": "UTC", "PATH": ""},
                )
            except BaseException:
                try:
                    os.write(2, b"exact-fd exec failed\n")
                finally:
                    os._exit(127)

        os.close(stdout_write)
        stdout_write = -1
        os.close(stderr_write)
        stderr_write = -1
        os.set_blocking(stdout_read, False)
        os.set_blocking(stderr_read, False)
        streams = {stdout_read: bytearray(), stderr_read: bytearray()}
        selector = selectors.DefaultSelector()
        selector.register(stdout_read, selectors.EVENT_READ)
        selector.register(stderr_read, selectors.EVENT_READ)
        deadline = time.monotonic() + timeout_seconds
        overflow = False
        timed_out = False
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                break
            for key, _ in selector.select(min(remaining, 0.25)):
                try:
                    remaining_output = output_limit + 1 - len(streams[key.fd])
                    chunk = os.read(key.fd, min(8192, max(1, remaining_output)))
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(key.fd)
                    os.close(key.fd)
                    continue
                streams[key.fd].extend(chunk)
                if len(streams[key.fd]) > output_limit:
                    overflow = True
                    break
            if overflow:
                break
        status: int | None = None
        while not timed_out and not overflow and status is None:
            waited_pid, observed_status = wait_for_verifier_child(pid, os.WNOHANG)
            if waited_pid == pid:
                status = observed_status
                break
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                break
            time.sleep(min(remaining, 0.01))
        if timed_out or overflow:
            terminate_verifier_process_group(pid)
        if status is None:
            _, status = wait_for_verifier_child(pid)
        pid = -1
        returncode = os.waitstatus_to_exitcode(status)
        error = "verifier timeout" if timed_out else "verifier output limit exceeded" if overflow else None
        return returncode, bytes(streams[stdout_read]), bytes(streams[stderr_read]), error
    except OSError as exc:
        return 127, b"", b"", str(exc)
    finally:
        if pid > 0:
            terminate_verifier_process_group(pid)
            try:
                wait_for_verifier_child(pid)
            except OSError:
                pass
        if selector is not None:
            try:
                selector.close()
            except OSError:
                pass
        for descriptor in (stdout_read, stdout_write, stderr_read, stderr_write):
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass


def elf_self_test_fixture(
    elf_class: int = 2,
    data_encoding: int = 1,
    forbidden_dependency: str | None = None,
) -> bytes:
    """Construct a minimal bounded ELF image for parser regression tests."""
    byte_order = "<" if data_encoding == 1 else ">"
    if elf_class == 1:
        header_size = 52
        program_header_size = 32
        header_format = byte_order + "HHIIIIIHHHHHH"
        program_header_format = byte_order + "IIIIIIII"
        dynamic_format = byte_order + "iI"
        machine = 3
    else:
        header_size = 64
        program_header_size = 56
        header_format = byte_order + "HHIQQQIHHHHHH"
        program_header_format = byte_order + "IIQQQQQQ"
        dynamic_format = byte_order + "qQ"
        machine = 62
    extra = b""
    second_segment_type: int | None = None
    if forbidden_dependency == "PT_INTERP":
        extra = b"/unbound/loader\0"
        second_segment_type = 3
    elif forbidden_dependency == "DT_NEEDED":
        extra = struct.pack(dynamic_format, 1, 1) + struct.pack(dynamic_format, 0, 0)
        second_segment_type = 2
    elif forbidden_dependency is not None:
        raise ValueError(f"unknown ELF fixture dependency {forbidden_dependency}")
    program_header_count = 1 + int(second_segment_type is not None)
    extra_offset = header_size + program_header_count * program_header_size
    file_size = extra_offset + len(extra)
    identity = bytearray(16)
    identity[:4] = b"\x7fELF"
    identity[4] = elf_class
    identity[5] = data_encoding
    identity[6] = 1
    header = bytes(identity) + struct.pack(
        header_format,
        2,
        machine,
        1,
        0,
        header_size,
        0,
        0,
        header_size,
        program_header_size,
        program_header_count,
        0,
        0,
        0,
    )
    if elf_class == 1:
        load = struct.pack(program_header_format, 1, 0, 0, 0, file_size, file_size, 5, 1)
        dependency = (
            struct.pack(
                program_header_format,
                second_segment_type,
                extra_offset,
                0,
                0,
                len(extra),
                len(extra),
                4,
                1,
            )
            if second_segment_type is not None
            else b""
        )
    else:
        load = struct.pack(program_header_format, 1, 5, 0, 0, 0, file_size, file_size, 1)
        dependency = (
            struct.pack(
                program_header_format,
                second_segment_type,
                4,
                extra_offset,
                0,
                0,
                len(extra),
                len(extra),
                1,
            )
            if second_segment_type is not None
            else b""
        )
    return header + load + dependency + extra


def self_test_exceptional_process_group_cleanup(root: Path) -> bool:
    """Prove privileged post-fork failures cannot leave a live descendant."""
    if os.geteuid() != 0:
        return False
    if verifier_process_limit_is_enforceable():
        raise RuntimeError("privileged verifier dispatch was misclassified as process-bounded")

    source = root / "exception-verifier"
    shutil.copyfile("/bin/sh", source)
    source.chmod(0o555)
    source_fd = open_absolute_nofollow(source)
    sealed_fd = -1
    marker_read, marker_write = os.pipe()
    lifetime_read, lifetime_write = os.pipe()
    os.set_inheritable(marker_write, True)
    os.set_inheritable(lifetime_write, True)
    os.set_blocking(marker_read, False)
    os.set_blocking(lifetime_read, False)
    observed = bytearray()
    original_selector = selectors.DefaultSelector

    class InjectedParentFailure:
        def __init__(self) -> None:
            self.inner = original_selector()

        def register(self, *args: object, **kwargs: object) -> object:
            return self.inner.register(*args, **kwargs)

        def unregister(self, *args: object, **kwargs: object) -> object:
            return self.inner.unregister(*args, **kwargs)

        def get_map(self) -> object:
            return self.inner.get_map()

        def close(self) -> None:
            self.inner.close()

        def select(self, timeout: float | None = None) -> object:
            del timeout
            deadline = time.monotonic() + 3.0
            while len(observed.split()) != 2:
                try:
                    chunk = os.read(marker_read, 128)
                except BlockingIOError:
                    chunk = None
                if chunk:
                    observed.extend(chunk)
                elif chunk == b"":
                    raise RuntimeError("descendant fixture closed before reporting readiness")
                if time.monotonic() >= deadline:
                    raise RuntimeError("descendant fixture did not become ready")
                time.sleep(0.005)
            raise OSError(errno.EIO, "injected parent-side selector failure")

    script = (
        "( exec 1>&- 2>&-; while :; do :; done ) & child=$!; "
        f'printf "%s %s\\n" "$$" "$child" >&{marker_write}; '
        "exec 1>&- 2>&-; while :; do :; done"
    )
    result: tuple[int, bytes, bytes, str | None] | None = None
    leader = -1
    group_closed = False
    try:
        try:
            sealed_fd = clone_to_sealed_executable_fd(source_fd)
            selectors.DefaultSelector = InjectedParentFailure
            result = run_sealed_exact_fd(
                sealed_fd,
                ["ephemeral-authority-verifier", "-c", script],
                timeout_seconds=30.0,
                output_limit=1024,
            )
        finally:
            selectors.DefaultSelector = original_selector
            for descriptor in (marker_write, marker_read, lifetime_write, sealed_fd, source_fd):
                if descriptor >= 0:
                    try:
                        os.close(descriptor)
                    except OSError:
                        pass

        if result is None or result[0] != 127 or result[3] != "[Errno 5] injected parent-side selector failure":
            raise RuntimeError("post-fork exception fixture did not reach the injected failure")
        leader, _ = map(int, observed.split())
        deadline = time.monotonic() + 1.0
        while True:
            try:
                lifetime = os.read(lifetime_read, 1)
            except BlockingIOError:
                lifetime = None
            if lifetime == b"":
                group_closed = True
                break
            if time.monotonic() >= deadline:
                raise RuntimeError("post-fork exception left a live verifier descendant")
            time.sleep(0.005)
    finally:
        if leader > 0 and not group_closed:
            try:
                os.killpg(leader, signal.SIGKILL)
            except OSError:
                pass
        try:
            os.close(lifetime_read)
        except OSError:
            pass
    return True


def self_test_authority_fd_exec() -> None:
    """Exercise no-follow opening and exact-object dispatch without package writes."""
    with tempfile.TemporaryDirectory(prefix="artifact-authority-self-test-") as raw_root:
        root = Path(raw_root).resolve()
        real_parent = root / "real"
        real_parent.mkdir()
        payload = real_parent / "payload"
        payload.write_bytes(b"policy-v1")

        payload_fd = open_absolute_nofollow(payload)
        try:
            observed = read_stable_regular_fd(payload_fd, 64)
            os.replace(payload, real_parent / "replaced-policy")
            payload.write_bytes(b"policy-v2")
            if observed != b"policy-v1":
                raise RuntimeError("one-open policy bytes changed after pathname replacement")
        finally:
            os.close(payload_fd)

        final_link = real_parent / "final-link"
        final_link.symlink_to(payload)
        try:
            descriptor = open_absolute_nofollow(final_link)
        except OSError:
            pass
        else:
            os.close(descriptor)
            raise RuntimeError("no-follow open accepted a final-component symlink")

        parent_link = root / "parent-link"
        parent_link.symlink_to(real_parent, target_is_directory=True)
        try:
            descriptor = open_absolute_nofollow(parent_link / "payload")
        except OSError:
            pass
        else:
            os.close(descriptor)
            raise RuntimeError("no-follow open accepted a parent-component symlink")

        accepted_fixture_count = 0
        for elf_class in (1, 2):
            for data_encoding in (1, 2):
                fixture = root / f"static-elf-{elf_class}-{data_encoding}"
                fixture.write_bytes(elf_self_test_fixture(elf_class, data_encoding))
                fixture.chmod(0o555)
                descriptor = open_absolute_nofollow(fixture)
                try:
                    hash_stable_executable_fd(descriptor)
                finally:
                    os.close(descriptor)
                accepted_fixture_count += 1

        valid_elf = elf_self_test_fixture()
        malformed_header = bytearray(valid_elf)
        struct.pack_into("<H", malformed_header, 52, 0)
        out_of_bounds_table = bytearray(valid_elf)
        struct.pack_into("<Q", out_of_bounds_table, 32, len(valid_elf) + 1)
        out_of_bounds_segment = bytearray(valid_elf)
        struct.pack_into("<Q", out_of_bounds_segment, 64 + 32, len(valid_elf) + 1)
        unsupported_class = bytearray(valid_elf)
        unsupported_class[4] = 3
        unsupported_byte_order = bytearray(valid_elf)
        unsupported_byte_order[5] = 3
        rejected_fixtures = {
            "truncated": b"\x7fELF\x02\x01\x01",
            "unsupported-class": bytes(unsupported_class),
            "unsupported-byte-order": bytes(unsupported_byte_order),
            "malformed-header": bytes(malformed_header),
            "out-of-bounds-program-table": bytes(out_of_bounds_table),
            "out-of-bounds-segment": bytes(out_of_bounds_segment),
            "pt-interp": elf_self_test_fixture(forbidden_dependency="PT_INTERP"),
            "dt-needed": elf_self_test_fixture(forbidden_dependency="DT_NEEDED"),
        }
        rejected_fixture_count = 0
        for name, image in rejected_fixtures.items():
            fixture = root / f"rejected-{name}"
            fixture.write_bytes(image)
            fixture.chmod(0o555)
            descriptor = open_absolute_nofollow(fixture)
            try:
                try:
                    hash_stable_executable_fd(descriptor)
                except OSError:
                    rejected_fixture_count += 1
                else:
                    raise RuntimeError(f"self-contained verifier parser accepted {name}")
            finally:
                os.close(descriptor)
        if (accepted_fixture_count, rejected_fixture_count) != (4, len(rejected_fixtures)):
            raise RuntimeError("ELF dependency-closure self-test coverage drift")

        if not sealed_fd_exec_supported():
            print(
                "PASS authority exact-fd self-test: static ELF closure accepted, "
                "dynamic/malformed ELF rejected, sealed protected dispatch fail-closed on this platform"
            )
            return

        executable = root / "verifier"
        in_place_image = root / "in-place-image"
        replacement = root / "replacement"
        shutil.copyfile("/bin/echo", executable)
        shutil.copyfile("/bin/false", in_place_image)
        shutil.copyfile("/bin/false", replacement)
        executable.chmod(0o555)
        in_place_image.chmod(0o555)
        replacement.chmod(0o555)
        source_fd = open_absolute_nofollow(executable)
        sealed_fd = -1
        try:
            source_inode = os.fstat(source_fd).st_ino
            sealed_fd = clone_to_sealed_executable_fd(source_fd)
            before = hash_stable_executable_fd(sealed_fd, require_self_contained=False)
            executable.chmod(0o755)
            shutil.copyfile(in_place_image, executable)
            executable.chmod(0o555)
            if executable.stat().st_ino != source_inode:
                raise RuntimeError("self-test did not modify the verifier source inode in place")
            os.replace(replacement, executable)
            os.lseek(sealed_fd, 0, os.SEEK_SET)
            try:
                os.write(sealed_fd, b"x")
            except OSError as exc:
                if exc.errno != errno.EPERM:
                    raise
            else:
                raise RuntimeError("sealed verifier accepted an in-place byte write")
            try:
                os.ftruncate(sealed_fd, 0)
            except OSError as exc:
                if exc.errno != errno.EPERM:
                    raise
            else:
                raise RuntimeError("sealed verifier accepted truncation")
            returncode, stdout, stderr, error = run_sealed_exact_fd(
                sealed_fd,
                ["ephemeral-authority-verifier", "PASS"],
                timeout_seconds=5.0,
                output_limit=1024,
            )
            after = hash_stable_executable_fd(sealed_fd, require_self_contained=False)
        finally:
            os.close(source_fd)
            if sealed_fd >= 0:
                os.close(sealed_fd)
        if before != after:
            raise RuntimeError("sealed verifier changed after source mutation or pathname replacement")
        if (returncode, stdout, stderr, error) != (0, b"PASS\n", b"", None):
            raise RuntimeError("sealed hashed verifier descriptor was not the executed object")

        timeout_source = root / "timeout-verifier"
        shutil.copyfile("/bin/sh", timeout_source)
        timeout_source.chmod(0o555)
        timeout_source_fd = open_absolute_nofollow(timeout_source)
        timeout_sealed_fd = -1
        try:
            timeout_sealed_fd = clone_to_sealed_executable_fd(timeout_source_fd)
            started = time.monotonic()
            timeout_result = run_sealed_exact_fd(
                timeout_sealed_fd,
                [
                    "ephemeral-authority-verifier",
                    "-c",
                    "exec 1>&- 2>&-; while :; do :; done",
                ],
                timeout_seconds=0.1,
                output_limit=1024,
            )
            elapsed = time.monotonic() - started
        finally:
            os.close(timeout_source_fd)
            if timeout_sealed_fd >= 0:
                os.close(timeout_sealed_fd)
        if timeout_result[3] != "verifier timeout" or elapsed > 2.0:
            raise RuntimeError("verifier watchdog did not survive early output-pipe closure")
        privileged_group_fixture = self_test_exceptional_process_group_cleanup(root)
    print(
        "PASS authority exact-fd self-test: static ELF closure accepted, dynamic/malformed ELF "
        "rejected, sealed writes/truncation rejected, the hashed clone executed after source "
        "mutation and pathname replacement, the watchdog survived closed output pipes, and "
        + (
            "privileged exceptional process-group cleanup passed"
            if privileged_group_fixture
            else "the privileged process-group fixture was not applicable"
        )
    )


def is_digest(value: object) -> bool:
    return isinstance(value, str) and DIGEST.fullmatch(value) is not None


def is_timestamp(value: object) -> bool:
    if not isinstance(value, str) or TIMESTAMP.fullmatch(value) is None:
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    return True


def is_gate_lineage(gate_id: str, value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(rf"{re.escape(gate_id)}-r\d{{4}}", value) is not None


def pass_effect(
    gate_id: str,
    acceptance: dict,
    gate_ids: list[str],
    gate_by_id: dict[str, dict],
    gate_index: dict[str, int],
) -> str | None:
    output_ids = frozenset(
        row.get("id")
        for row in acceptance.get("accepted_outputs", [])
        if isinstance(row, dict)
    )
    matches = [
        output_set
        for output_set in gate_by_id[gate_id].get("pass_output_sets", [])
        if isinstance(output_set, list) and frozenset(output_set) == output_ids
    ]
    if len(matches) != 1:
        return None
    if output_ids == {"NO_WINNER"}:
        return "TERMINAL_NO_WINNER"
    index = gate_index[gate_id]
    if index == len(gate_ids) - 1:
        return "MANDATORY_DAG_COMPLETE"
    next_gate_id = gate_ids[index + 1]
    if gate_by_id[gate_id]["phase_id"] == gate_by_id[next_gate_id]["phase_id"]:
        return "PUBLISH_NEXT_GATE"
    return "WAIT_FOR_NEXT_PHASE_AUTHORITY"


def is_invalidation_receipt(row: dict) -> bool:
    path = row.get("path")
    digest = row.get("sha256")
    match = INVALIDATION_RECEIPT_PATH.fullmatch(path) if isinstance(path, str) else None
    return (
        match is not None
        and row.get("role") == "invalidation trigger receipt"
        and is_digest(digest)
        and match.group(1) == digest
    )


def packet_lifecycle_pair_is_legal(maturity: object, disposition: object) -> bool:
    if disposition == "NOT_RUN":
        return maturity in {"DRAFT", "INPUT_LOCKED", "SEALED"}
    return disposition in GATE_STATUSES - {"NOT_RUN"} and maturity == "SEALED"


def git(path: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(path), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def regular_files(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


def schema_semantic_projection(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: schema_semantic_projection(member)
            for key, member in value.items()
            if key not in SCHEMA_ANNOTATION_KEYS
        }
    if isinstance(value, list):
        return [schema_semantic_projection(member) for member in value]
    return value


def schema_semantic_sha256(schema: dict) -> str:
    payload = json.dumps(
        schema_semantic_projection(schema),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def nested_object(value: object, *members: str) -> dict | None:
    cursor = value
    for member in members:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(member)
    return cursor if isinstance(cursor, dict) else None


def packet_path(gate: dict) -> Path:
    return EXECUTION_ROOT / f"phase-{gate['phase_id']}" / gate["id"]


def instantiated_gate_ids(state: dict, gate_ids: list[str]) -> list[str]:
    count = state.get("instantiated_gate_count")
    if not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= len(gate_ids):
        return []
    return gate_ids[:count]


def archive_relative_path(row: dict) -> Path:
    return Path("history") / f"{row.get('gate_id')}--{row.get('manifest_sha256')}"


def archive_path(row: dict) -> Path:
    return EXECUTION_ROOT / archive_relative_path(row)


def validate_schema_files(validation: Validation) -> None:
    schema_root = EXECUTION_ROOT / "schemas"
    validation.require(regular_files(schema_root) == SCHEMA_NAMES, "schema file set drift")
    expected_root_fields = {
        "gate-catalog.schema.json": CATALOG_KEYS,
        "execution-state.schema.json": STATE_KEYS,
        "manifest.schema.json": MANIFEST_KEYS,
        "acceptance.schema.json": ACCEPTANCE_KEYS,
        "input-lock.schema.json": INPUT_LOCK_KEYS,
        "phase-entry-attestation.schema.json": PHASE_ENTRY_ATTESTATION_KEYS,
    }
    schemas: dict[str, dict] = {}
    for name in sorted(SCHEMA_NAMES):
        schema = load_json(schema_root / name, validation)
        schemas[name] = schema
        validation.require(
            schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
            f"{name} must declare JSON Schema draft 2020-12",
        )
        validation.require(schema.get("$id") == name, f"{name} $id drift")
        validation.require(schema.get("type") == "object", f"{name} root type must be object")
        validation.require(schema.get("additionalProperties") is False, f"{name} must reject unknown root fields")
        validation.require(set(schema.get("properties", {})) == expected_root_fields[name], f"{name} root property set drift")
        validation.require(set(schema.get("required", [])) == expected_root_fields[name], f"{name} required root field set drift")
        validation.require(
            schema_semantic_sha256(schema) == SCHEMA_SEMANTIC_SHA256[name],
            f"{name} semantic projection changed without validator-contract review",
        )

    packet_cardinality_projections = (
        (
            nested_object(schemas.get("manifest.schema.json", {}), "properties", "artifacts"),
            "manifest artifact floor",
        ),
        (
            nested_object(schemas.get("input-lock.schema.json", {}), "properties", "entries"),
            "input-lock entry floor",
        ),
    )
    for schema_object, label in packet_cardinality_projections:
        validation.require(
            isinstance(schema_object, dict)
            and schema_object.get("minItems") == len(CONTROLLED_PACKET_FILES),
            f"{label} must equal the controlled packet-file cardinality",
        )

    state_schema = schemas.get("execution-state.schema.json", {})
    topology_cardinality_keywords = (
        (
            nested_object(state_schema, "properties", "instantiated_gate_count"),
            "maximum",
            "execution-state instantiated count",
        ),
        (
            nested_object(state_schema, "$defs", "invalidationEvent", "properties", "affected"),
            "maxItems",
            "execution-state invalidation suffix",
        ),
        (
            nested_object(state_schema, "$defs", "transition", "properties", "prior_packets"),
            "maxItems",
            "execution-state prior frontier",
        ),
    )
    for schema_object, keyword, label in topology_cardinality_keywords:
        validation.require(
            isinstance(schema_object, dict) and keyword not in schema_object,
            f"{label} must derive cardinality from gates.json, not a schema literal",
        )


def validate_catalog(
    validation: Validation,
) -> tuple[dict, list[dict], list[str], list[str], dict[str, dict], dict[str, int]]:
    catalog = load_json(EXECUTION_ROOT / "gates.json", validation)
    validation.require(set(catalog) == CATALOG_KEYS, "gate catalog root field set drift")
    validation.require(catalog.get("$schema") == "schemas/gate-catalog.schema.json", "gate catalog schema reference drift")
    validation.require(catalog.get("schema_version") == 1, "gate catalog schema_version must be 1")

    phases = catalog.get("phases", [])
    gates = catalog.get("gates", [])
    validation.require(isinstance(phases, list) and bool(phases), "phase array must be nonempty")
    validation.require(isinstance(gates, list) and bool(gates), "gate array must be nonempty")

    phase_ids: list[str] = []
    if isinstance(phases, list) and phases:
        phase_keys = {
            "id",
            "capability_ceiling",
            "entry_condition",
        }
        for index, phase in enumerate(phases):
            label = f"phase row {index + 1}"
            validation.require(isinstance(phase, dict) and set(phase) == phase_keys, f"{label} field set drift")
            if not isinstance(phase, dict):
                continue
            phase_id = phase.get("id")
            valid_phase_id = isinstance(phase_id, str) and PHASE_ID.fullmatch(phase_id) is not None
            validation.require(valid_phase_id, f"{label} id malformed")
            if valid_phase_id:
                phase_ids.append(phase_id)
            for field in ("capability_ceiling", "entry_condition"):
                validation.require(isinstance(phase.get(field), str) and bool(phase[field]), f"{label} {field} missing")
        validation.require(len(phase_ids) == len(set(phase_ids)), "phase ids must be unique")
        validation.require(
            phase_ids == [f"{index:02d}" for index in range(len(phases))],
            "phase ids must be contiguous, ordered, and zero-based",
        )

    gate_rows = gates if isinstance(gates, list) else []
    gate_ids: list[str] = []
    gate_by_id: dict[str, dict] = {}
    if isinstance(gates, list) and gates:
        gate_keys = {
            "id",
            "phase_id",
            "pass_output_sets",
        }
        seen_ids: set[str] = set()
        previous_phase_index = -1
        phases_seen: set[str] = set()
        for index, gate in enumerate(gates):
            label = f"gate row {index + 1}"
            validation.require(isinstance(gate, dict) and set(gate) == gate_keys, f"{label} field set drift")
            if not isinstance(gate, dict):
                continue
            gate_id = gate.get("id")
            phase_id = gate.get("phase_id")
            gate_match = GATE_ID.fullmatch(gate_id) if isinstance(gate_id, str) else None
            valid_gate_id = gate_match is not None
            validation.require(valid_gate_id, f"{label} id malformed")
            validation.require(phase_id in phase_ids, f"{label} phase unknown")
            if not valid_gate_id or phase_id not in phase_ids:
                continue
            gate_ids.append(gate_id)
            validation.require(gate_id not in seen_ids, f"duplicate gate id {gate_id}")
            seen_ids.add(gate_id)
            gate_by_id[gate_id] = gate
            validation.require(gate_match.group("phase") == phase_id, f"gate {gate_id} id does not encode phase {phase_id}")
            phase_index = phase_ids.index(phase_id)
            validation.require(phase_index >= previous_phase_index, f"gate {gate_id} moves backward across phases")
            previous_phase_index = phase_index
            phases_seen.add(phase_id)
            pass_output_sets = gate.get("pass_output_sets")
            validation.require(
                isinstance(pass_output_sets, list) and bool(pass_output_sets),
                f"gate {gate_id} must declare a nonempty PASS output-set array",
            )
            seen_output_sets: set[frozenset[str]] = set()
            if not isinstance(pass_output_sets, list):
                continue
            for output_set_index, output_ids in enumerate(pass_output_sets):
                valid_outputs = (
                    isinstance(output_ids, list)
                    and bool(output_ids)
                    and all(isinstance(output_id, str) and bool(output_id) for output_id in output_ids)
                    and len(output_ids) == len(set(output_ids))
                )
                validation.require(valid_outputs, f"gate {gate_id} PASS output set {output_set_index} is malformed or internally duplicated")
                if valid_outputs:
                    output_set = frozenset(output_ids)
                    validation.require(output_set not in seen_output_sets, f"gate {gate_id} has ambiguous duplicate PASS output sets")
                    seen_output_sets.add(output_set)
                    if "NO_WINNER" in output_set:
                        validation.require(output_ids == ["NO_WINNER"], f"gate {gate_id} NO_WINNER PASS output set must contain only NO_WINNER")

        validation.require(phases_seen == set(phase_ids), "every catalog phase must contain at least one gate")
        if len(gate_ids) == len(gates) and len(gate_by_id) == len(gates):
            for index, gate_id in enumerate(gate_ids):
                gate = gate_by_id[gate_id]
                output_sets = gate.get("pass_output_sets", [])
                has_continuation = any(
                    isinstance(output_set, list) and frozenset(output_set) != {"NO_WINNER"}
                    for output_set in output_sets
                )
                if index == len(gate_ids) - 1:
                    validation.require(
                        all(isinstance(output_set, list) and "NO_WINNER" not in output_set for output_set in output_sets),
                        f"final gate {gate_id} cannot terminate as NO_WINNER",
                    )
                    continue
                validation.require(has_continuation, f"non-final gate {gate_id} omits a PASS output set that continues the causal chain")

    gate_index = {gate_id: index for index, gate_id in enumerate(gate_ids)}
    return catalog, gate_rows, phase_ids, gate_ids, gate_by_id, gate_index


def validate_state(
    validation: Validation,
    gate_ids: list[str],
    gate_by_id: dict[str, dict],
    gate_index: dict[str, int],
    state_path: Path | None = None,
    seen_state_digests: set[str] | None = None,
    seen_operation_ids: set[str] | None = None,
    depth: int = 0,
) -> dict:
    source = state_path or EXECUTION_ROOT / "state.json"
    state = load_json(source, validation)
    label = source.relative_to(EXECUTION_ROOT).as_posix()
    validation.require(depth <= 64, "execution state history exceeds the bounded 64-transition limit")
    if depth > 64:
        return state
    if seen_state_digests is None:
        seen_state_digests = {sha256(source)}
    if seen_operation_ids is None:
        seen_operation_ids = set()
    validation.require(set(state) == STATE_KEYS, f"execution state field set drift: {label}")
    validation.require(state.get("$schema") == "schemas/execution-state.schema.json", f"execution state schema reference drift: {label}")
    validation.require(state.get("schema_version") == 2, f"execution state schema_version must be 2: {label}")
    validation.require(state.get("catalog_sha256") == sha256(EXECUTION_ROOT / "gates.json"), f"execution state catalog digest mismatch: {label}")

    instantiated_count = state.get("instantiated_gate_count")
    count_valid = (
        isinstance(instantiated_count, int)
        and not isinstance(instantiated_count, bool)
        and 1 <= instantiated_count <= len(gate_ids)
    )
    validation.require(count_valid, "instantiated gate count must select a nonempty exact causal prefix")

    invalidations = state.get("invalidations")
    validation.require(isinstance(invalidations, list), "invalidations must be an array")
    seen_archives: set[str] = set()
    seen_triggers: set[str] = set()
    if isinstance(invalidations, list):
        for index, event in enumerate(invalidations):
            validation.require(isinstance(event, dict) and set(event) == INVALIDATION_KEYS, f"invalidation event {index} field set drift")
            if not isinstance(event, dict):
                continue
            trigger = event.get("trigger_sha256")
            validation.require(is_digest(trigger), f"invalidation event {index} trigger digest malformed")
            validation.require(trigger not in seen_triggers, f"invalidation event {index} reuses an earlier trigger digest")
            if is_digest(trigger):
                seen_triggers.add(trigger)
            recorded_at = str(event.get("recorded_at", ""))
            validation.require(is_timestamp(recorded_at), f"invalidation event {index} timestamp malformed")
            affected = event.get("affected")
            validation.require(isinstance(affected, list) and bool(affected), f"invalidation event {index} affected closure missing")
            affected_gate_ids: list[str] = []
            if not isinstance(affected, list):
                continue
            for archive_index, archive in enumerate(affected):
                validation.require(isinstance(archive, dict) and set(archive) == ARCHIVE_KEYS, f"invalidation event {index} archive {archive_index} field set drift")
                if not isinstance(archive, dict):
                    continue
                gate_id = archive.get("gate_id")
                affected_gate_ids.append(str(gate_id))
                validation.require(gate_id in gate_by_id, f"invalidation event {index} archive {archive_index} gate id unknown")
                for field in ("manifest_sha256", "acceptance_sha256"):
                    validation.require(is_digest(archive.get(field)), f"invalidation event {index} archive {archive_index} {field} malformed")
                expected_archive = archive_relative_path(archive).as_posix()
                validation.require(expected_archive not in seen_archives, f"duplicate invalidation archive {expected_archive}")
                seen_archives.add(expected_archive)
            if affected_gate_ids and affected_gate_ids[0] in gate_index and affected_gate_ids[-1] in gate_index:
                earliest = affected_gate_ids[0]
                last_affected = affected_gate_ids[-1]
                start = gate_index[earliest]
                end = gate_index[last_affected] + 1
                validation.require(start <= end - 1, f"invalidation event {index} affected range is reversed")
                validation.require(affected_gate_ids == gate_ids[start:end], f"invalidation event {index} must archive the complete causal range {earliest} through {last_affected}")

    transition = state.get("transition")
    if transition is None:
        validation.require(instantiated_count == 1, "only the exact one-packet bootstrap may omit a state transition")
        validation.require(invalidations == [], "bootstrap state may not contain invalidations")
        return state

    valid_transition = isinstance(transition, dict) and set(transition) == STATE_TRANSITION_KEYS
    validation.require(valid_transition, "execution state transition field set drift")
    if not valid_transition:
        return state

    kind = transition.get("kind")
    validation.require(kind in {"ADVANCE", "INVALIDATE"}, "execution state transition kind invalid")
    prior_digest = transition.get("prior_state_sha256")
    validation.require(is_digest(prior_digest), "execution state prior-state digest malformed")
    validation.require(is_timestamp(transition.get("published_at")), "execution state publication timestamp malformed")
    publisher = validate_principal(
        transition.get("published_by"),
        ACTION_PRINCIPAL_KEYS,
        "execution state publisher",
        validation,
    )

    prior_packets = transition.get("prior_packets")
    valid_prior_packets = isinstance(prior_packets, list) and 1 <= len(prior_packets) <= len(gate_ids)
    validation.require(valid_prior_packets, "execution state transition requires a bounded nonempty prior packet frontier")
    prior_gate_ids: list[str] = []
    if isinstance(prior_packets, list):
        for position, row in enumerate(prior_packets):
            valid_row = isinstance(row, dict) and set(row) == PACKET_IDENTITY_KEYS
            validation.require(valid_row, f"execution state prior packet {position} field set drift")
            if not valid_row:
                continue
            gate_id = str(row.get("gate_id"))
            prior_gate_ids.append(gate_id)
            validation.require(gate_id in gate_by_id, f"execution state prior packet {position} gate unknown")
            validation.require(is_gate_lineage(gate_id, row.get("lineage_id")), f"execution state prior packet {position} lineage malformed")
            validation.require(is_digest(row.get("manifest_sha256")), f"execution state prior packet {position} manifest digest malformed")
            validation.require(is_digest(row.get("acceptance_sha256")), f"execution state prior packet {position} acceptance digest malformed")
        validation.require(
            prior_gate_ids == gate_ids[: len(prior_packets)],
            "execution state prior_packets must name the exact complete prior causal prefix",
        )

    replacement = transition.get("replacement")
    valid_replacement = isinstance(replacement, dict) and set(replacement) == LINEAGE_IDENTITY_KEYS
    validation.require(valid_replacement, "execution state replacement identity malformed")
    replacement_gate = str(replacement.get("gate_id")) if isinstance(replacement, dict) else ""
    if valid_replacement:
        validation.require(replacement_gate in gate_by_id, "execution state replacement gate unknown")
        validation.require(is_gate_lineage(replacement_gate, replacement.get("lineage_id")), "execution state replacement lineage malformed")

    publication = transition.get("publication")
    valid_publication = isinstance(publication, dict) and set(publication) == PUBLICATION_KEYS
    validation.require(valid_publication, "execution state publication intent field set drift")
    publication_authority: tuple[str, str, str] | None = None
    if valid_publication:
        method = publication.get("method")
        validation.require(method in {"CONDITIONAL_WRITE", "EXCLUSIVE_LEASE"}, "execution state publication method invalid")
        for field in ("operation_id", "prior_token"):
            value = publication.get(field)
            validation.require(isinstance(value, str) and BOUNDED_TOKEN.fullmatch(value) is not None, f"execution state publication {field} malformed")
        operation_id = publication.get("operation_id")
        validation.require(operation_id not in seen_operation_ids, "execution state publication operation_id is reused in retained history")
        if isinstance(operation_id, str):
            seen_operation_ids.add(operation_id)
        publication_authority = validate_principal(
            publication.get("authority"),
            PRINCIPAL_KEYS,
            "execution state publication authority",
            validation,
        )
        if method == "CONDITIONAL_WRITE":
            validation.require(publication.get("lease_id") is None and publication.get("fencing_token") is None, "conditional state write may not claim lease fields")
        elif method == "EXCLUSIVE_LEASE":
            lease_id = publication.get("lease_id")
            fencing_token = publication.get("fencing_token")
            validation.require(isinstance(lease_id, str) and BOUNDED_TOKEN.fullmatch(lease_id) is not None, "exclusive state lease id malformed")
            validation.require(isinstance(fencing_token, int) and not isinstance(fencing_token, bool) and fencing_token >= 0, "exclusive state fencing token malformed")
    validation.require(
        principals_are_axis_independent(publisher, publication_authority),
        "state publisher and commit authority must differ on all three identity axes",
    )

    if valid_prior_packets and replacement_gate in gate_index and count_valid:
        prior_count = len(prior_packets)
        replacement_index = gate_index[replacement_gate]
        if kind == "ADVANCE":
            validation.require(replacement_index == prior_count, "ADVANCE must instantiate the exact next gate after the authenticated prior frontier")
            validation.require(instantiated_count == prior_count + 1, "ADVANCE state count must add exactly one gate")
        elif kind == "INVALIDATE":
            validation.require(isinstance(invalidations, list) and bool(invalidations), "INVALIDATE requires one appended invalidation event")
            event = invalidations[-1] if isinstance(invalidations, list) and invalidations else None
            affected = event.get("affected") if isinstance(event, dict) else None
            affected_ids = [str(row.get("gate_id")) for row in affected if isinstance(row, dict)] if isinstance(affected, list) else []
            expected_suffix = gate_ids[replacement_index:prior_count]
            validation.require(affected_ids == expected_suffix, "INVALIDATE must archive the entire suffix through the authenticated prior frontier")
            validation.require(instantiated_count == replacement_index + 1, "INVALIDATE state count must end at the exact replacement gate")
            validation.require(event is not None and event.get("recorded_at") == transition.get("published_at"), "invalidation time must equal its authenticated state publication time")

    if is_digest(prior_digest):
        prior_path = HISTORY_ROOT / "states" / f"{prior_digest}.json"
        validation.require(prior_digest not in seen_state_digests, "execution state history contains a digest cycle")
        validation.require(prior_path.is_file(), "execution state prior bytes are not retained by digest")
        if prior_path.is_file() and prior_digest not in seen_state_digests:
            seen_state_digests.add(str(prior_digest))
            validation.require(sha256(prior_path) == prior_digest, "execution state retained prior bytes digest mismatch")
            prior_state = load_json(prior_path, validation)
            validation.require(set(prior_state) == STATE_KEYS, "retained prior execution state field set drift")
            validation.require(prior_state.get("schema_version") == 2, "retained prior execution state version drift")
            validation.require(prior_state.get("catalog_sha256") == state.get("catalog_sha256"), "retained prior state catalog drift")
            validation.require(prior_state.get("instantiated_gate_count") == len(prior_packets) if isinstance(prior_packets, list) else False, "authenticated prior packet frontier count differs from retained prior state")
            if kind == "ADVANCE":
                validation.require(prior_state.get("invalidations") == invalidations, "ADVANCE may not rewrite invalidation history")
            elif kind == "INVALIDATE" and isinstance(invalidations, list):
                validation.require(prior_state.get("invalidations") == invalidations[:-1], "INVALIDATE must append exactly one event to prior history")
            validate_state(
                validation,
                gate_ids,
                gate_by_id,
                gate_index,
                state_path=prior_path,
                seen_state_digests=seen_state_digests,
                seen_operation_ids=seen_operation_ids,
                depth=depth + 1,
            )
    return state


def validate_packet_layout(
    state: dict,
    gates: list[dict],
    phase_ids: list[str],
    gate_ids: list[str],
    gate_by_id: dict[str, dict],
    validation: Validation,
) -> None:
    validation.require(regular_files(TEMPLATE_ROOT) == REQUIRED_PACKET_FILES, "packet-template file set drift")
    validation.require(not any(path.is_dir() for path in TEMPLATE_ROOT.rglob("*")), "packet-template may not contain placeholder directories")
    instantiated = instantiated_gate_ids(state, gate_ids)
    instantiated_set = set(instantiated)

    for gate in gates:
        if not isinstance(gate, dict) or gate.get("id") not in gate_by_id:
            continue
        gate_id = gate["id"]
        packet = packet_path(gate)
        if gate_id in instantiated_set:
            validation.require(packet.is_dir(), f"instantiated packet missing: {packet.relative_to(PLAN_ROOT)}")
            if packet.is_dir():
                missing = REQUIRED_PACKET_FILES - regular_files(packet)
                validation.require(not missing, f"instantiated packet missing required files: {sorted(missing)}")
        else:
            validation.require(not packet.exists(), f"future packet instantiated before eligibility: {packet.relative_to(PLAN_ROOT)}")

    for phase_id in phase_ids:
        phase_root = EXECUTION_ROOT / f"phase-{phase_id}"
        expected_children = {
            gate_id
            for gate_id in instantiated_set
            if gate_id in gate_by_id and gate_by_id[gate_id]["phase_id"] == phase_id
        }
        if expected_children:
            validation.require(phase_root.is_dir(), f"phase-{phase_id} container missing")
            if phase_root.is_dir():
                actual_children = {path.name for path in phase_root.iterdir()}
                validation.require(actual_children == expected_children, f"phase-{phase_id} canonical child set drift")
        else:
            validation.require(not phase_root.exists(), f"empty/future phase-{phase_id} container is forbidden")

    invalidations = state.get("invalidations", [])
    has_history = bool(invalidations) or state.get("transition") is not None
    if has_history:
        validation.require(HISTORY_ROOT.is_dir(), "history directory missing for declared state lineage")
        declared_files: set[str] = set()
        for event in invalidations:
            if not isinstance(event, dict):
                continue
            for row in event.get("affected", []):
                if not isinstance(row, dict):
                    continue
                relative_archive = archive_relative_path(row)
                archive = archive_path(row)
                validation.require(archive.is_dir(), f"declared archive missing: {relative_archive}")
                if archive.is_dir():
                    declared_files |= {
                        (relative_archive.relative_to("history") / path).as_posix()
                        for path in regular_files(archive)
                    }

        cursor = state
        seen_state_digests: set[str] = set()
        for depth in range(66):
            transition = cursor.get("transition")
            if transition is None:
                break
            if not isinstance(transition, dict) or not is_digest(transition.get("prior_state_sha256")):
                break
            prior_digest = str(transition["prior_state_sha256"])
            validation.require(prior_digest not in seen_state_digests, "execution state history contains a digest cycle")
            if prior_digest in seen_state_digests:
                break
            seen_state_digests.add(prior_digest)
            relative = Path("states") / f"{prior_digest}.json"
            prior_path = HISTORY_ROOT / relative
            declared_files.add(relative.as_posix())
            if not prior_path.is_file():
                break
            cursor = load_json(prior_path, validation)
        else:
            validation.require(False, "execution state history exceeds the bounded 65-transition chain")

        validation.require(regular_files(HISTORY_ROOT) == declared_files, "undeclared or missing history files")
    else:
        validation.require(not HISTORY_ROOT.exists(), "history directory is forbidden for the exact bootstrap state")

    allowed_top = {
        "README.md",
        "gates.json",
        "state.json",
        "validate.py",
        "schemas",
        "packet-template",
        "history",
        *(f"phase-{phase_id}" for phase_id in phase_ids),
    }
    actual_top = {path.name for path in EXECUTION_ROOT.iterdir()}
    validation.require(actual_top <= allowed_top, f"undeclared execution-root entries: {sorted(actual_top - allowed_top)}")


def validate_manifest_shape(
    manifest: dict,
    source: Path,
    template: bool,
    gate_by_id: dict[str, dict],
    validation: Validation,
) -> None:
    label = "template" if template else source.relative_to(PLAN_ROOT).as_posix()
    validation.require(set(manifest) == MANIFEST_KEYS, f"manifest field set drift: {label}")
    validation.require(manifest.get("schema_version") == 3, f"manifest schema_version drift: {label}")
    expected_schema = "../schemas/manifest.schema.json" if template else "../../schemas/manifest.schema.json"
    validation.require(manifest.get("$schema") == expected_schema, f"manifest schema reference drift: {label}")
    maturity = manifest.get("packet_maturity")
    reported_status = manifest.get("reported_status")
    validation.require(maturity in {"TEMPLATE", "DRAFT", "INPUT_LOCKED", "SEALED"}, f"invalid packet maturity: {label}")
    validation.require(reported_status in GATE_STATUSES, f"invalid producer-reported status: {label}")
    if template:
        validation.require(maturity == "TEMPLATE", f"template manifest maturity drift: {label}")
    else:
        validation.require(maturity in {"DRAFT", "INPUT_LOCKED", "SEALED"}, f"instantiated packet cannot retain template maturity: {label}")
    if maturity in {"DRAFT", "INPUT_LOCKED"}:
        validation.require(reported_status == "NOT_RUN", f"pre-result packet must report NOT_RUN: {label}")
    elif maturity == "SEALED":
        validation.require(reported_status in {"PARTIAL", "PASS", "FAIL", "BLOCKED"}, f"SEALED packet requires a final producer report: {label}")
    report_detail = manifest.get("report_detail")
    validation.require(isinstance(report_detail, str) and bool(report_detail), f"producer report requires exact detail: {label}")
    generated_at = manifest.get("generated_at")
    validation.require(generated_at is None or is_timestamp(generated_at), f"manifest generated_at malformed: {label}")
    digest = manifest.get("catalog_sha256")
    validation.require(digest is None or is_digest(digest), f"manifest catalog digest malformed: {label}")
    input_lock_digest = manifest.get("input_lock_sha256")
    validation.require(input_lock_digest is None or is_digest(input_lock_digest), f"manifest input-lock digest malformed: {label}")
    producer = manifest.get("producer")
    if maturity == "SEALED":
        validate_principal(
            producer,
            ACTION_PRINCIPAL_KEYS,
            f"sealed manifest result producer: {label}",
            validation,
        )
        validation.require(is_timestamp(generated_at), f"sealed manifest production time malformed: {label}")
    else:
        validation.require(producer is None, f"pre-result manifest must not contain a result producer: {label}")
    lineage = manifest.get("lineage_id")
    validation.require(lineage == "TEMPLATE" if template else bool(LINEAGE.fullmatch(str(lineage))), f"manifest lineage id malformed: {label}")
    if template:
        validation.require(generated_at is None, f"template manifest generated_at must be null: {label}")
        validation.require(digest is None, f"template manifest catalog digest must be null: {label}")
        validation.require(manifest.get("source_context") == [], f"template manifest source_context must be empty: {label}")
    else:
        validation.require(is_timestamp(generated_at), f"live manifest generated_at required: {label}")
        validation.require(is_digest(digest), f"live manifest catalog digest required: {label}")
        validation.require(isinstance(manifest.get("source_context"), list) and bool(manifest["source_context"]), f"live manifest source_context cannot be empty: {label}")

    predecessors = manifest.get("predecessors")
    validation.require(isinstance(predecessors, list) and len(predecessors) <= 1, f"manifest predecessor set malformed: {label}")
    if isinstance(predecessors, list):
        for row in predecessors:
            valid_row = isinstance(row, dict) and set(row) == {"gate_id", "lineage_id", "manifest_sha256", "acceptance_sha256"}
            validation.require(valid_row, f"manifest predecessor row malformed: {label}")
            if valid_row:
                validation.require(row["gate_id"] in gate_by_id, f"manifest predecessor gate unknown: {label}")
                validation.require(is_gate_lineage(str(row["gate_id"]), row["lineage_id"]), f"manifest predecessor lineage malformed or names another gate: {label}")
                validation.require(is_digest(row["manifest_sha256"]), f"manifest predecessor digest malformed: {label}")
                validation.require(is_digest(row["acceptance_sha256"]), f"acceptance predecessor digest malformed: {label}")

    artifacts = manifest.get("artifacts")
    validation.require(isinstance(artifacts, list) and bool(artifacts), f"manifest artifacts missing: {label}")
    seen_artifacts: set[str] = set()
    if isinstance(artifacts, list):
        for row in artifacts:
            valid_row = isinstance(row, dict) and set(row) == {"path", "role", "sha256"}
            validation.require(valid_row, f"manifest artifact row malformed: {label}")
            if not valid_row:
                continue
            path = row["path"]
            safe = isinstance(path, str) and bool(path) and not Path(path).is_absolute() and ".." not in Path(path).parts and Path(path).as_posix() == path
            validation.require(safe, f"unsafe manifest artifact path {path!r}: {label}")
            validation.require(path not in seen_artifacts, f"duplicate manifest artifact path {path!r}: {label}")
            seen_artifacts.add(path)
            validation.require(isinstance(row["role"], str) and bool(row["role"]), f"manifest artifact role missing: {label}")
            if template:
                validation.require(row["sha256"] is None, f"template artifact must not have a digest: {label}/{path}")
            else:
                validation.require(is_digest(row["sha256"]), f"instantiated artifact digest malformed: {label}/{path}")

    outputs = manifest.get("outputs")
    validation.require(isinstance(outputs, list), f"manifest outputs must be an array: {label}")
    seen_outputs: set[str] = set()
    if isinstance(outputs, list):
        for row in outputs:
            valid_row = isinstance(row, dict) and set(row) == {"id", "state", "sha256"}
            validation.require(valid_row, f"manifest output row malformed: {label}")
            if not valid_row:
                continue
            output_id = row["id"]
            validation.require(isinstance(output_id, str) and bool(output_id), f"manifest output id missing: {label}")
            validation.require(output_id not in seen_outputs, f"duplicate manifest output id {output_id!r}: {label}")
            seen_outputs.add(output_id)
            validation.require(row["state"] in {"EXPECTED", "PRODUCED", "NOT_APPLICABLE"}, f"manifest output state invalid: {label}/{output_id}")
            if row["state"] == "PRODUCED":
                validation.require(is_digest(row["sha256"]), f"PRODUCED output digest malformed: {label}/{output_id}")
            else:
                validation.require(row["sha256"] is None, f"unproduced output must not have a digest: {label}/{output_id}")

def validate_acceptance_shape(acceptance: dict, source: Path, template: bool, validation: Validation) -> None:
    label = "template" if template else source.relative_to(PLAN_ROOT).as_posix()
    validation.require(set(acceptance) == ACCEPTANCE_KEYS, f"acceptance field set drift: {label}")
    validation.require(acceptance.get("schema_version") == 2, f"acceptance schema_version drift: {label}")
    expected_schema = "../schemas/acceptance.schema.json" if template else "../../schemas/acceptance.schema.json"
    validation.require(acceptance.get("$schema") == expected_schema, f"acceptance schema reference drift: {label}")
    disposition = acceptance.get("disposition")
    validation.require(disposition in GATE_STATUSES, f"invalid independent verdict: {label}")
    validation.require(acceptance.get("lineage_id") == "TEMPLATE" if template else bool(LINEAGE.fullmatch(str(acceptance.get("lineage_id", "")))), f"acceptance lineage malformed: {label}")

    outputs = acceptance.get("accepted_outputs")
    validation.require(isinstance(outputs, list), f"accepted_outputs must be an array: {label}")
    seen_outputs: set[str] = set()
    if isinstance(outputs, list):
        for row in outputs:
            valid_row = isinstance(row, dict) and set(row) == {"id", "sha256"}
            validation.require(valid_row, f"accepted output row malformed: {label}")
            if valid_row:
                validation.require(isinstance(row["id"], str) and bool(row["id"]), f"accepted output id missing: {label}")
                validation.require(row["id"] not in seen_outputs, f"duplicate accepted output id: {label}/{row['id']}")
                seen_outputs.add(row["id"])
                validation.require(is_digest(row["sha256"]), f"accepted output digest malformed: {label}/{row['id']}")

    if disposition == "NOT_RUN":
        validation.require(acceptance.get("disposition_detail") is None, f"NOT_RUN acceptance detail must be null: {label}")
        validation.require(acceptance.get("manifest_sha256") is None, f"NOT_RUN acceptance must not name a manifest: {label}")
        validation.require(outputs == [], f"NOT_RUN acceptance must contain no outputs: {label}")
        validation.require(acceptance.get("accepted_by") is None, f"NOT_RUN acceptance must contain no acceptor: {label}")
        validation.require(acceptance.get("accepted_at") is None, f"NOT_RUN acceptance must contain no time: {label}")
    elif disposition in GATE_STATUSES:
        validation.require(is_digest(acceptance.get("manifest_sha256")), f"final verdict manifest digest malformed: {label}")
        detail = acceptance.get("disposition_detail")
        validation.require(isinstance(detail, str) and bool(detail), f"{disposition} verdict requires exact detail: {label}")
        acceptor = acceptance.get("accepted_by")
        validate_principal(
            acceptor,
            ACTION_PRINCIPAL_KEYS,
            f"final verdict acceptor: {label}",
            validation,
        )
        validation.require(is_timestamp(acceptance.get("accepted_at")), f"final verdict time malformed: {label}")
        if disposition == "PASS":
            validation.require(isinstance(outputs, list) and bool(outputs), f"PASS must accept at least one exact output: {label}")
        else:
            validation.require(outputs == [], f"non-PASS verdict must accept no output: {label}")


def validate_template(gate_by_id: dict[str, dict], validation: Validation) -> None:
    manifest_path = TEMPLATE_ROOT / "manifest.json"
    acceptance_path = TEMPLATE_ROOT / "acceptance.json"
    manifest = load_json(manifest_path, validation)
    acceptance = load_json(acceptance_path, validation)
    validate_manifest_shape(manifest, manifest_path, True, gate_by_id, validation)
    validate_acceptance_shape(acceptance, acceptance_path, True, validation)
    validate_packet_document(TEMPLATE_ROOT / "packet.md", True, "TEMPLATE", validation)
    validation.require(manifest.get("phase_id") == manifest.get("gate_id") == manifest.get("lineage_id") == "TEMPLATE", "template manifest identity drift")
    validation.require(manifest.get("packet_maturity") == "TEMPLATE" and manifest.get("reported_status") == "NOT_RUN", "template manifest state drift")
    validation.require(manifest.get("catalog_sha256") is None, "template manifest must not pin a live catalog")
    validation.require(manifest.get("predecessors") == [] and manifest.get("input_lock_sha256") is None, "template manifest must not pin live dependencies")
    validation.require(manifest.get("producer") is None, "template manifest must not claim result production")
    artifact_rows = manifest.get("artifacts", [])
    artifact_paths = {row.get("path") for row in artifact_rows if isinstance(row, dict)}
    validation.require(artifact_paths == CONTROLLED_PACKET_FILES, "template controlled artifact list drift")
    validation.require(all(row.get("sha256") is None for row in artifact_rows if isinstance(row, dict)), "template artifacts must be unhashed rows")
    validation.require(manifest.get("outputs") == [], "template manifest must not predict gate outputs")
    validation.require(acceptance.get("phase_id") == acceptance.get("gate_id") == acceptance.get("lineage_id") == "TEMPLATE", "template acceptance identity drift")
    validation.require(acceptance.get("disposition") == "NOT_RUN", "template acceptance must remain NOT_RUN")


def validate_source_context(manifest: dict, live: bool, validation: Validation) -> None:
    contexts = manifest.get("source_context")
    validation.require(isinstance(contexts, list), "source_context must be an array")
    if not isinstance(contexts, list):
        return
    seen_roles: set[str] = set()
    for context in contexts:
        keys = {"role", "path", "branch", "head", "dirty", "notes"}
        validation.require(isinstance(context, dict) and set(context) == keys, "source context row malformed")
        if not isinstance(context, dict):
            continue
        role = context.get("role")
        validation.require(isinstance(role, str) and bool(role) and role not in seen_roles, f"source context role missing/duplicate: {role}")
        if isinstance(role, str):
            seen_roles.add(role)
        path = Path(str(context.get("path", "")))
        validation.require(path.is_absolute(), f"source context path must be absolute: {path}")
        validation.require(context.get("branch") is None or isinstance(context.get("branch"), str), f"source context branch malformed: {path}")
        validation.require(context.get("head") is None or bool(GIT_OBJECT_ID.fullmatch(str(context.get("head")))), f"source context HEAD malformed: {path}")
        validation.require(isinstance(context.get("dirty"), bool), f"source context dirty flag malformed: {path}")
        validation.require(isinstance(context.get("notes"), str), f"source context notes malformed: {path}")
        if not live:
            continue
        validation.require(path.is_dir(), f"live source context path missing: {path}")
        validation.require(context.get("head") is not None, f"live source context HEAD missing: {path}")
        if not path.is_dir() or context.get("head") is None:
            continue
        try:
            git(path, "cat-file", "-e", f"{context['head']}^{{commit}}")
        except subprocess.CalledProcessError as exc:
            validation.require(False, f"source commit cannot be resolved in {path}: {exc}")
            continue
        try:
            branch = git(path, "rev-parse", "--abbrev-ref", "HEAD")
            head = git(path, "rev-parse", "HEAD")
            dirty = bool(git(path, "status", "--porcelain"))
        except subprocess.CalledProcessError as exc:
            validation.require(False, f"cannot inspect live source context {path}: {exc}")
            continue
        validation.require(context.get("branch") == branch, f"live source branch drift: {path}")
        validation.require(context.get("head") == head, f"live source HEAD drift: {path}")
        validation.require(context.get("dirty") is dirty, f"live source dirty-state drift: {path}")
        if role == "reserved product implementation base":
            try:
                upstream = git(path, "rev-parse", "origin/main")
            except subprocess.CalledProcessError as exc:
                validation.require(False, f"cannot resolve reserved product origin/main: {exc}")
            else:
                validation.require(upstream == head, "reserved product HEAD no longer matches local origin/main")


def validate_heading_regions(
    region: str,
    headings: tuple[str, ...],
    label: str,
    validation: Validation,
) -> None:
    positions = [region.find(heading) for heading in headings]
    validation.require(all(position >= 0 for position in positions), f"required heading missing: {label}")
    validation.require(positions == sorted(positions) and len(set(positions)) == len(headings), f"required heading order drift: {label}")
    validation.require(all(region.count(heading) == 1 for heading in headings), f"required heading duplicated: {label}")
    if not all(position >= 0 for position in positions) or positions != sorted(positions):
        return
    for index, heading in enumerate(headings):
        start = positions[index] + len(heading)
        end = positions[index + 1] if index + 1 < len(headings) else len(region)
        substantive = re.sub(r"\s+", "", region[start:end])
        validation.require(len(substantive) >= 40, f"heading has no substantive responsibility body: {label}/{heading}")


def read_packet_sections(path: Path, validation: Validation) -> dict[str, str]:
    """Split one packet document into five exact, independently checked regions."""
    label = path.relative_to(PLAN_ROOT).as_posix()
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        validation.require(False, f"cannot read packet contract {label}: {exc}")
        return {}
    positions = [content.find(marker) for marker in PACKET_SECTION_MARKERS]
    validation.require(all(position >= 0 for position in positions), f"packet section marker missing: {label}")
    validation.require(
        positions == sorted(positions) and len(set(positions)) == len(PACKET_SECTION_MARKERS),
        f"packet section order drift: {label}",
    )
    validation.require(
        all(content.count(marker) == 1 for marker in PACKET_SECTION_MARKERS),
        f"packet section marker duplicated: {label}",
    )
    if not all(position >= 0 for position in positions) or positions != sorted(positions):
        return {}
    validation.require(not content[:positions[0]].strip(), f"content precedes the first packet marker: {label}")
    validation.require(
        not content[positions[-1] + len(PACKET_SECTION_MARKERS[-1]):].strip(),
        f"content follows the terminal packet marker: {label}",
    )
    sections: dict[str, str] = {}
    for index, name in enumerate(PACKET_SECTION_NAMES):
        start = positions[index] + len(PACKET_SECTION_MARKERS[index])
        end = positions[index + 1]
        region = content[start:end]
        validation.require(
            len(re.sub(r"\s+", "", region)) >= 200,
            f"packet responsibility is semantically empty: {label}/{name}",
        )
        sections[name] = region
    return sections


def validate_anchor_section(
    content: str,
    anchors: tuple[str, ...],
    label: str,
    validation: Validation,
) -> None:
    """Keep a fused responsibility independently machine-detectable."""
    folded = content.casefold()
    for anchor in anchors:
        validation.require(anchor.casefold() in folded, f"section omits responsibility anchor {anchor!r}: {label}")


def validate_plan_note(
    content: str,
    label: str,
    template: bool,
    maturity: object,
    validation: Validation,
) -> None:
    """Enforce one frozen plan with independently detectable spec/decision regions."""
    positions = [content.find(marker) for marker in PLAN_SECTION_MARKERS]
    validation.require(all(position >= 0 for position in positions), f"plan section marker missing: {label}")
    validation.require(positions == sorted(positions) and len(set(positions)) == 3, f"plan section order drift: {label}")
    validation.require(all(content.count(marker) == 1 for marker in PLAN_SECTION_MARKERS), f"plan section marker duplicated: {label}")
    if not all(position >= 0 for position in positions) or positions != sorted(positions):
        return
    validation.require(
        not content[positions[2] + len(PLAN_SECTION_MARKERS[2]):].strip(),
        f"content follows the terminal plan marker: {label}",
    )
    spec_region = content[positions[0] + len(PLAN_SECTION_MARKERS[0]):positions[1]]
    decision_region = content[positions[1] + len(PLAN_SECTION_MARKERS[1]):positions[2]]
    validation.require(len(re.sub(r"\s+", "", spec_region)) >= 200, f"plan specification responsibility is semantically empty: {label}")
    validation.require(len(re.sub(r"\s+", "", decision_region)) >= 200, f"plan decision responsibility is semantically empty: {label}")
    validate_heading_regions(spec_region, PLAN_SPEC_HEADINGS, f"{label}/spec", validation)
    validate_heading_regions(decision_region, PLAN_DECISION_HEADINGS, f"{label}/decisions", validation)
    for token in (
        "manifest.json",
        "evidence/input-lock.json",
        "objective",
        "non-goals",
        "success",
        "scope",
        "disposition",
        "DAG",
        "stop",
        "cap",
        "cleanup",
        "outputs",
        "consumer",
        "handoff",
        "execution/state.json",
        "invalidation",
        "reopening",
    ):
        validation.require(token.lower() in spec_region.lower(), f"plan specification omits responsibility anchor {token!r}: {label}")
    for token in (
        "ledger",
        "OPEN",
        "ACCEPTED",
        "alternatives",
        "evidence",
        "owner",
        "independent acceptor",
        "new lineage",
        "downstream",
        "invalidates",
    ):
        validation.require(token.lower() in decision_region.lower(), f"plan decisions omit responsibility anchor {token!r}: {label}")
    if not template:
        validation.require("TEMPLATE" not in content, f"live plan retains template authority: {label}")
    if maturity in {"INPUT_LOCKED", "SEALED"}:
        unresolved_rows = [
            line
            for line in decision_region.splitlines()
            if line.startswith("|") and ("| `OPEN` |" in line or "`UNDECIDED`" in line)
        ]
        validation.require(not unresolved_rows, f"locked plan retains execution-changing OPEN/UNDECIDED rows: {label}")


def validate_evaluation_note(
    content: str,
    label: str,
    template: bool,
    validation: Validation,
) -> None:
    """Enforce the fused evaluation note's two nonempty responsibility regions."""
    positions = [content.find(marker) for marker in EVALUATION_SECTION_MARKERS]
    validation.require(all(position >= 0 for position in positions), f"evaluation section marker missing: {label}")
    validation.require(positions == sorted(positions) and len(set(positions)) == 3, f"evaluation section order drift: {label}")
    validation.require(all(content.count(marker) == 1 for marker in EVALUATION_SECTION_MARKERS), f"evaluation section marker duplicated: {label}")
    if not all(position >= 0 for position in positions) or positions != sorted(positions):
        return
    experiment_region = content[positions[0] + len(EVALUATION_SECTION_MARKERS[0]):positions[1]]
    benchmark_region = content[positions[1] + len(EVALUATION_SECTION_MARKERS[1]):positions[2]]
    for token in ("Protocol", "preregistration", "Raw-result", "Results"):
        validation.require(token in experiment_region, f"evaluation experiment responsibility omits {token!r}: {label}")
    for token in ("Benchmark", "comparator", "statistics", "uncertainty", "Operation cost matrix"):
        validation.require(token in benchmark_region, f"evaluation benchmark responsibility omits {token!r}: {label}")
    validation.require(len(experiment_region.strip()) >= 200, f"evaluation experiment responsibility is semantically empty: {label}")
    validation.require(len(benchmark_region.strip()) >= 200, f"evaluation benchmark responsibility is semantically empty: {label}")
    if not template:
        validation.require("TEMPLATE" not in content, f"live evaluation contract retains template authority: {label}")


def validate_packet_document(
    path: Path,
    template: bool,
    maturity: object,
    validation: Validation,
) -> None:
    """Validate one three-file packet's fused human contract."""
    label = path.relative_to(PLAN_ROOT).as_posix()
    sections = read_packet_sections(path, validation)
    if set(sections) != set(PACKET_SECTION_NAMES):
        return
    validate_plan_note(sections["plan"], f"{label}/plan", template, maturity, validation)
    validate_anchor_section(
        sections["algorithms"],
        ALGORITHM_SECTION_ANCHORS,
        f"{label}/algorithms",
        validation,
    )
    validate_evaluation_note(
        sections["evaluation"],
        f"{label}/evaluation",
        template,
        validation,
    )
    validate_anchor_section(
        sections["verification"],
        VERIFICATION_SECTION_ANCHORS,
        f"{label}/verification",
        validation,
    )
    validate_anchor_section(
        sections["handoff"],
        HANDOFF_SECTION_ANCHORS,
        f"{label}/handoff",
        validation,
    )


def validate_phase_entry_attestation(
    attestation_path: Path,
    authorization_path: Path,
    manifest: dict,
    gate_by_id: dict[str, dict],
    validation: Validation,
) -> dict:
    """Validate phase authority structurally; external policy authenticates it later."""
    gate_id = str(manifest.get("gate_id", "UNKNOWN"))
    attestation = load_json(attestation_path, validation)
    validation.require(set(attestation) == PHASE_ENTRY_ATTESTATION_KEYS, f"phase-entry attestation field set drift: {gate_id}")
    validation.require(attestation.get("$schema") == "phase-entry-attestation.schema.json", f"phase-entry attestation schema reference drift: {gate_id}")
    validation.require(attestation.get("schema_version") == 2, f"phase-entry attestation schema_version drift: {gate_id}")
    for field in ("catalog_sha256", "phase_id", "gate_id", "lineage_id"):
        validation.require(attestation.get(field) == manifest.get(field), f"phase-entry attestation {field} does not bind its manifest: {gate_id}")
    validation.require(
        attestation.get("authorization_receipt_sha256") == sha256(authorization_path),
        f"phase-entry attestation does not bind exact authorization receipt: {gate_id}",
    )

    phase_id = str(attestation.get("phase_id", ""))
    phase_gate_ids = sorted(
        candidate_gate_id
        for candidate_gate_id, candidate_gate in gate_by_id.items()
        if candidate_gate.get("phase_id") == phase_id
    )
    actors = attestation.get("authorized_actors")
    required_capabilities, observed_capabilities, capability_conflicts = (
        phase_capability_contract(actors, phase_gate_ids)
    )
    validation.require(isinstance(actors, list) and bool(actors), f"phase-entry authorized actor set missing: {gate_id}")
    actor_principals: list[tuple[str, str, str]] = []
    if isinstance(actors, list):
        for index, actor in enumerate(actors):
            principal = validate_principal(
                actor,
                ACTOR_KEYS,
                f"phase-entry actor {index}: {gate_id}",
                validation,
            )
            if principal is not None:
                actor_principals.append(principal)
            capabilities = actor.get("capabilities") if isinstance(actor, dict) else None
            valid_capabilities = (
                isinstance(capabilities, list)
                and bool(capabilities)
                and capabilities == sorted(capabilities)
                and len(capabilities) == len(set(capabilities))
            )
            validation.require(valid_capabilities, f"phase-entry actor {index} capability set malformed: {gate_id}")
            if not isinstance(capabilities, list):
                continue
            for capability in capabilities:
                match = re.fullmatch(r"(produce|accept):(.+)", str(capability))
                capability_gate = match.group(2) if match else ""
                validation.require(match is not None, f"unknown phase capability {capability!r}: {gate_id}")
                validation.require(capability_gate in gate_by_id, f"phase capability names unknown gate {capability_gate!r}: {gate_id}")
                if capability_gate in gate_by_id:
                    validation.require(
                        gate_by_id[capability_gate]["phase_id"] == phase_id,
                        f"phase capability escapes attested phase: {gate_id}/{capability}",
                    )
    missing_capabilities = sorted(required_capabilities - observed_capabilities)
    unexpected_capabilities = sorted(observed_capabilities - required_capabilities)
    validation.require(
        observed_capabilities == required_capabilities,
        "phase-entry capability union does not exactly cover the phase: "
        f"{gate_id}; missing={missing_capabilities!r}; unexpected={unexpected_capabilities!r}",
    )
    validation.require(
        not capability_conflicts,
        f"phase-entry actors hold both sides of one gate: {gate_id}/{capability_conflicts!r}",
    )
    validation.require(len(actor_principals) == len(set(actor_principals)), f"phase-entry actor triples duplicated: {gate_id}")
    for axis, label in enumerate(("principal IDs", "credentials", "control domains")):
        validation.require(
            len({principal[axis] for principal in actor_principals}) == len(actor_principals),
            f"phase-entry actor {label} duplicated: {gate_id}",
        )

    authorizer = validate_principal(
        attestation.get("authorizer"),
        ACTION_PRINCIPAL_KEYS,
        f"phase-entry authorizer: {gate_id}",
        validation,
    )
    for actor in actor_principals:
        validation.require(
            principals_are_axis_independent(authorizer, actor),
            f"phase-entry authorizer overlaps an authorized actor: {gate_id}",
        )

    validity = attestation.get("validity")
    validity_keys = {
        "issued_at",
        "not_before",
        "expires_at",
        "revocation_checked_at",
        "revocation_status",
        "revocation_evidence_sha256",
    }
    valid_validity = isinstance(validity, dict) and set(validity) == validity_keys
    validation.require(valid_validity, f"phase-entry validity record malformed: {gate_id}")
    if valid_validity:
        for field in ("issued_at", "not_before", "expires_at", "revocation_checked_at"):
            validation.require(is_timestamp(validity.get(field)), f"phase-entry {field} malformed: {gate_id}")
        validation.require(validity.get("revocation_status") == "GOOD", f"phase-entry authority is revoked or unknown: {gate_id}")
        validation.require(is_digest(validity.get("revocation_evidence_sha256")), f"phase-entry revocation evidence digest malformed: {gate_id}")
        if all(is_timestamp(validity.get(field)) for field in ("issued_at", "not_before", "expires_at", "revocation_checked_at")):
            issued = datetime.strptime(validity["issued_at"], "%Y-%m-%dT%H:%M:%SZ")
            not_before = datetime.strptime(validity["not_before"], "%Y-%m-%dT%H:%M:%SZ")
            expires = datetime.strptime(validity["expires_at"], "%Y-%m-%dT%H:%M:%SZ")
            checked = datetime.strptime(validity["revocation_checked_at"], "%Y-%m-%dT%H:%M:%SZ")
            validation.require(issued <= not_before < expires, f"phase-entry validity interval is empty or reversed: {gate_id}")
            validation.require(not_before <= checked < expires, f"phase-entry revocation check lies outside validity: {gate_id}")
    return attestation


def validate_input_lock(
    packet: Path,
    manifest: dict,
    phase_entry: bool,
    gate_by_id: dict[str, dict],
    validation: Validation,
) -> dict | None:
    """Validate the acyclic pre-result lock and every immutable snapshot it names."""
    gate_id = str(manifest.get("gate_id", "UNKNOWN"))
    maturity = manifest.get("packet_maturity")
    claimed_digest = manifest.get("input_lock_sha256")
    evidence_root = packet / "evidence"
    lock_path = evidence_root / "input-lock.json"

    if claimed_digest is None:
        validation.require(not lock_path.exists(), f"unclaimed input-lock index exists: {gate_id}")
        validation.require(maturity == "DRAFT", f"only a DRAFT packet may omit the input lock: {gate_id}")
        return None

    validation.require(is_digest(claimed_digest), f"input-lock digest malformed: {gate_id}")
    validation.require(maturity in {"INPUT_LOCKED", "SEALED"}, f"input-lock digest requires INPUT_LOCKED or SEALED maturity: {gate_id}")
    validation.require(lock_path.is_file(), f"claimed input-lock index missing: {gate_id}")
    if not lock_path.is_file():
        return None
    validation.require(sha256(lock_path) == claimed_digest, f"input-lock index digest mismatch: {gate_id}")

    lock = load_json(lock_path, validation)
    validation.require(set(lock) == INPUT_LOCK_KEYS, f"input-lock field set drift: {gate_id}")
    validation.require(lock.get("$schema") == "../../../schemas/input-lock.schema.json", f"input-lock schema reference drift: {gate_id}")
    validation.require(lock.get("schema_version") == 2, f"input-lock schema_version drift: {gate_id}")
    for field in ("phase_id", "gate_id", "lineage_id", "catalog_sha256"):
        validation.require(lock.get(field) == manifest.get(field), f"input-lock {field} does not bind its manifest: {gate_id}")
    validation.require(is_timestamp(lock.get("locked_at")), f"input-lock timestamp malformed: {gate_id}")
    validate_principal(
        lock.get("producer"),
        ACTION_PRINCIPAL_KEYS,
        f"input-lock producer: {gate_id}",
        validation,
    )
    validation.require(lock.get("predecessors") == manifest.get("predecessors"), f"input-lock predecessor identities drift from manifest: {gate_id}")

    entries = lock.get("entries")
    validation.require(isinstance(entries, list) and len(entries) >= len(CONTROLLED_PACKET_FILES), f"input-lock entries must include every pre-result packet artifact: {gate_id}")
    if not isinstance(entries, list):
        return lock
    logical_paths: list[str] = []
    snapshot_paths: list[str] = []
    for index, row in enumerate(entries):
        valid_row = isinstance(row, dict) and set(row) == {"logical_path", "snapshot_path", "role", "sha256"}
        validation.require(valid_row, f"input-lock entry {index} malformed: {gate_id}")
        if not valid_row:
            continue
        logical_path = row["logical_path"]
        snapshot_path = row["snapshot_path"]
        logical_safe = isinstance(logical_path, str) and bool(logical_path) and not Path(logical_path).is_absolute() and ".." not in Path(logical_path).parts and Path(logical_path).as_posix() == logical_path
        snapshot_safe = isinstance(snapshot_path, str) and snapshot_path.startswith("input-lock/snapshots/") and not Path(snapshot_path).is_absolute() and ".." not in Path(snapshot_path).parts and Path(snapshot_path).as_posix() == snapshot_path
        validation.require(logical_safe, f"unsafe input-lock logical path {logical_path!r}: {gate_id}")
        validation.require(snapshot_safe, f"unsafe input-lock snapshot path {snapshot_path!r}: {gate_id}")
        validation.require(isinstance(row["role"], str) and bool(row["role"]), f"input-lock entry role missing: {gate_id}/{logical_path}")
        validation.require(is_digest(row["sha256"]), f"input-lock entry digest malformed: {gate_id}/{logical_path}")
        if isinstance(logical_path, str):
            logical_paths.append(logical_path)
        if isinstance(snapshot_path, str):
            snapshot_paths.append(snapshot_path)
            target = evidence_root / snapshot_path
            validation.require(target.is_file(), f"input-lock snapshot missing: {gate_id}/{snapshot_path}")
            if target.is_file() and is_digest(row["sha256"]):
                validation.require(sha256(target) == row["sha256"], f"input-lock snapshot digest mismatch: {gate_id}/{snapshot_path}")
                current = packet / str(logical_path)
                if logical_path in CONTROLLED_PACKET_FILES:
                    validation.require(current.is_file(), f"input-lock controlled source missing: {gate_id}/{logical_path}")
                    if current.is_file():
                        validation.require(sha256(current) == row["sha256"], f"controlled artifact changed after input lock: {gate_id}/{logical_path}")
                if logical_path == "packet.md":
                    validate_packet_document(target, False, str(maturity), validation)

    validation.require(logical_paths == sorted(logical_paths), f"input-lock entries must be sorted by logical_path: {gate_id}")
    validation.require(len(logical_paths) == len(set(logical_paths)), f"duplicate input-lock logical path: {gate_id}")
    validation.require(len(snapshot_paths) == len(set(snapshot_paths)), f"duplicate input-lock snapshot path: {gate_id}")
    validation.require(CONTROLLED_PACKET_FILES <= set(logical_paths), f"input-lock omits a required pre-result packet artifact: {gate_id}")
    authority_paths = {path for path in logical_paths if path.startswith("authority/")}
    if phase_entry:
        authority_path = f"authority/phase-{manifest.get('phase_id')}-authorization.receipt"
        attestation_path = f"authority/phase-{manifest.get('phase_id')}-entry-attestation.json"
        rows_by_logical_path = {
            row.get("logical_path"): row
            for row in entries
            if isinstance(row, dict) and isinstance(row.get("logical_path"), str)
        }
        authority_rows = [row for row in entries if isinstance(row, dict) and row.get("logical_path") == authority_path]
        attestation_rows = [row for row in entries if isinstance(row, dict) and row.get("logical_path") == attestation_path]
        validation.require(len(authority_rows) == 1, f"phase-entry input lock omits separate authority receipt: {gate_id}")
        if len(authority_rows) == 1:
            validation.require(authority_rows[0].get("role") == "phase authorization receipt", f"phase-entry authority receipt role drift: {gate_id}")
        validation.require(len(attestation_rows) == 1, f"phase-entry input lock omits phase-entry authorization attestation: {gate_id}")
        if len(attestation_rows) == 1:
            validation.require(attestation_rows[0].get("role") == "phase entry authorization attestation", f"phase-entry authorization attestation role drift: {gate_id}")
        if len(authority_rows) == 1 and len(attestation_rows) == 1:
            authority_snapshot = evidence_root / str(rows_by_logical_path[authority_path].get("snapshot_path"))
            attestation_snapshot = evidence_root / str(rows_by_logical_path[attestation_path].get("snapshot_path"))
            if authority_snapshot.is_file() and attestation_snapshot.is_file():
                validate_phase_entry_attestation(
                    attestation_snapshot,
                    authority_snapshot,
                    manifest,
                    gate_by_id,
                    validation,
                )
        validation.require(
            authority_paths == {authority_path, attestation_path},
            f"phase-entry authority snapshot set drift: {gate_id}",
        )
    else:
        validation.require(not authority_paths, f"same-phase input lock must inherit authority transitively: {gate_id}")
    snapshot_root = evidence_root / "input-lock" / "snapshots"
    actual_snapshots = {
        (Path("input-lock/snapshots") / path).as_posix()
        for path in regular_files(snapshot_root)
    }
    validation.require(set(snapshot_paths) == actual_snapshots, f"input-lock snapshot coverage drift: {gate_id}; missing={sorted(actual_snapshots - set(snapshot_paths))}, extra={sorted(set(snapshot_paths) - actual_snapshots)}")
    return lock


def validate_packet(
    packet: Path,
    gate_id: str,
    live: bool,
    resolve_predecessor: bool,
    gate_ids: list[str],
    gate_by_id: dict[str, dict],
    gate_index: dict[str, int],
    validation: Validation,
) -> tuple[dict, dict]:
    manifest_path = packet / "manifest.json"
    acceptance_path = packet / "acceptance.json"
    manifest = load_json(manifest_path, validation)
    acceptance = load_json(acceptance_path, validation)
    validate_manifest_shape(manifest, manifest_path, False, gate_by_id, validation)
    validate_acceptance_shape(acceptance, acceptance_path, False, validation)

    gate = gate_by_id[gate_id]
    expected_phase = gate["phase_id"]
    validation.require(manifest.get("phase_id") == expected_phase and manifest.get("gate_id") == gate_id, f"packet manifest identity drift: {gate_id}")
    validation.require(acceptance.get("phase_id") == expected_phase and acceptance.get("gate_id") == gate_id, f"packet acceptance identity drift: {gate_id}")
    validation.require(manifest.get("lineage_id") == acceptance.get("lineage_id"), f"packet lineage mismatch: {gate_id}")
    validation.require(is_gate_lineage(gate_id, manifest.get("lineage_id")), f"packet lineage must be prefixed by its exact gate id: {gate_id}")
    validation.require(manifest.get("catalog_sha256") == sha256(EXECUTION_ROOT / "gates.json"), f"packet catalog digest mismatch: {gate_id}")

    allowed_output_ids = {
        output_id
        for output_set in gate.get("pass_output_sets", [])
        for output_id in output_set
    }
    declared_output_ids = {
        row.get("id")
        for row in manifest.get("outputs", [])
        if isinstance(row, dict)
    }
    validation.require(declared_output_ids <= allowed_output_ids, f"packet declares an output outside the gate contract: {gate_id}")
    if manifest.get("packet_maturity") in {"DRAFT", "INPUT_LOCKED"}:
        validation.require(declared_output_ids == allowed_output_ids, f"pre-result packet must declare every catalog output: {gate_id}")
        validation.require(
            all(row.get("state") == "EXPECTED" for row in manifest.get("outputs", []) if isinstance(row, dict)),
            f"pre-result packet outputs must all remain EXPECTED: {gate_id}",
        )

    expected_predecessors = [] if gate_index[gate_id] == 0 else [gate_ids[gate_index[gate_id] - 1]]
    predecessor_rows = manifest.get("predecessors", [])
    actual_predecessors = [row.get("gate_id") for row in predecessor_rows if isinstance(row, dict)] if isinstance(predecessor_rows, list) else []
    validation.require(actual_predecessors == expected_predecessors, f"packet predecessor identity drift: {gate_id}")
    if resolve_predecessor and expected_predecessors and isinstance(predecessor_rows, list) and predecessor_rows:
        predecessor_id = expected_predecessors[0]
        predecessor_packet = packet_path(gate_by_id[predecessor_id])
        predecessor_manifest = load_json(predecessor_packet / "manifest.json", validation)
        predecessor_acceptance = load_json(predecessor_packet / "acceptance.json", validation)
        row = predecessor_rows[0]
        validation.require(row.get("lineage_id") == predecessor_manifest.get("lineage_id"), f"predecessor lineage digest edge drift: {gate_id}")
        validation.require(row.get("manifest_sha256") == sha256(predecessor_packet / "manifest.json"), f"predecessor manifest digest edge drift: {gate_id}")
        validation.require(row.get("acceptance_sha256") == sha256(predecessor_packet / "acceptance.json"), f"predecessor acceptance digest edge drift: {gate_id}")
        validation.require(predecessor_acceptance.get("disposition") == "PASS", f"predecessor is not independently accepted: {gate_id}")

    files = regular_files(packet)
    validation.require(REQUIRED_PACKET_FILES <= files, f"packet omits a required persistent file: {gate_id}")
    validate_packet_document(packet / "packet.md", False, str(manifest.get("packet_maturity")), validation)
    unexpected_root_files = {
        path
        for path in files - REQUIRED_PACKET_FILES
        if not path.startswith("evidence/")
    }
    validation.require(not unexpected_root_files, f"packet has undeclared root files outside the three-file contract: {gate_id}/{sorted(unexpected_root_files)}")
    for directory in (path for path in packet.rglob("*") if path.is_dir()):
        relative_directory = directory.relative_to(packet)
        validation.require(relative_directory.parts[0] == "evidence", f"packet subdirectories are reserved for evidence: {gate_id}/{relative_directory}")
    controlled_files = files - {"manifest.json", "acceptance.json"}
    artifact_rows = manifest.get("artifacts", [])
    artifact_map: dict[str, dict] = {}
    if isinstance(artifact_rows, list):
        for row in artifact_rows:
            if not isinstance(row, dict) or not isinstance(row.get("path"), str):
                continue
            artifact_map[row["path"]] = row
    validation.require(set(artifact_map) == controlled_files, f"packet manifest path coverage drift: {gate_id}; missing={sorted(controlled_files - set(artifact_map))}, extra={sorted(set(artifact_map) - controlled_files)}")
    for path, row in artifact_map.items():
        target = packet / path
        validation.require(target.is_file(), f"controlled artifact missing: {gate_id}/{path}")
        if target.is_file():
            validation.require(row.get("sha256") == sha256(target), f"controlled artifact digest mismatch: {gate_id}/{path}")
    controlled_digests = {
        row.get("sha256")
        for row in artifact_map.values()
        if is_digest(row.get("sha256"))
    }
    for output in manifest.get("outputs", []):
        if isinstance(output, dict) and output.get("state") == "PRODUCED":
            validation.require(output.get("sha256") in controlled_digests, f"produced output does not resolve to a controlled artifact: {gate_id}/{output.get('id')}")

    disposition = acceptance.get("disposition")
    validation.require(
        packet_lifecycle_pair_is_legal(manifest.get("packet_maturity"), disposition),
        f"illegal manifest/acceptance lifecycle pair: {gate_id}",
    )
    if disposition == "NOT_RUN":
        maturity = manifest.get("packet_maturity")
        if maturity in {"DRAFT", "INPUT_LOCKED"}:
            validation.require(manifest.get("reported_status") == "NOT_RUN", f"pre-result packet with NOT_RUN acceptance requires a NOT_RUN producer report: {gate_id}")
            produced = [row for row in manifest.get("outputs", []) if isinstance(row, dict) and row.get("state") == "PRODUCED"]
            validation.require(not produced, f"pre-result packet may not claim produced outputs: {gate_id}")
        if maturity == "DRAFT":
            draft_evidence = {
                path: row
                for path, row in artifact_map.items()
                if path.startswith("evidence/")
            }
            validation.require(all(is_invalidation_receipt(row) for row in draft_evidence.values()), f"DRAFT packet evidence is limited to content-addressed invalidation receipts: {gate_id}")
    elif disposition in GATE_STATUSES:
        validation.require(acceptance.get("manifest_sha256") == sha256(manifest_path), f"acceptance does not bind exact manifest: {gate_id}")
        if disposition == "PASS":
            validation.require(manifest.get("reported_status") == "PASS", f"independent PASS requires a producer-reported PASS: {gate_id}")
            validation.require(
                all(row.get("state") != "EXPECTED" for row in manifest.get("outputs", []) if isinstance(row, dict)),
                f"PASS packet may not retain an EXPECTED output: {gate_id}",
            )
            produced = {
                row["id"]: row["sha256"]
                for row in manifest.get("outputs", [])
                if isinstance(row, dict) and row.get("state") == "PRODUCED"
            }
            accepted = {
                row["id"]: row["sha256"]
                for row in acceptance.get("accepted_outputs", [])
                if isinstance(row, dict)
            }
            validation.require(accepted == produced and bool(produced), f"PASS output identities differ from produced outputs: {gate_id}")
            accepted_ids = set(accepted)
            allowed_sets = {
                frozenset(output_set)
                for output_set in gate.get("pass_output_sets", [])
            }
            validation.require(frozenset(accepted_ids) in allowed_sets, f"PASS output set is not an allowed transition: {gate_id}")

    predecessor_id = expected_predecessors[0] if expected_predecessors else None
    phase_entry = (
        predecessor_id is None
        or gate_by_id[predecessor_id]["phase_id"] != gate["phase_id"]
    )
    lock = validate_input_lock(packet, manifest, phase_entry, gate_by_id, validation)
    if manifest.get("packet_maturity") == "SEALED":
        manifest_producer = principal_tuple(manifest.get("producer"))
        lock_producer = principal_tuple(lock.get("producer")) if isinstance(lock, dict) else None
        validation.require(
            manifest_producer == lock_producer and manifest_producer is not None,
            f"sealed result producer must be the exact input-lock producer: {gate_id}",
        )
    validate_source_context(manifest, live=live and disposition == "NOT_RUN", validation=validation)

    for path in packet.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for marker in PLACEHOLDER_MARKERS:
            validation.require(marker not in text, f"template placeholder {marker!r} leaked into {path.relative_to(PLAN_ROOT)}")
    return manifest, acceptance


def validate_canonical_packets(
    state: dict,
    gate_ids: list[str],
    gate_by_id: dict[str, dict],
    gate_index: dict[str, int],
    validation: Validation,
) -> None:
    instantiated = instantiated_gate_ids(state, gate_ids)
    packets: dict[str, tuple[dict, dict]] = {}
    last_gate = instantiated[-1] if instantiated else None
    for gate_id in instantiated:
        if gate_id not in gate_by_id:
            continue
        packets[gate_id] = validate_packet(
            packet_path(gate_by_id[gate_id]),
            gate_id,
            live=(gate_id == last_gate),
            resolve_predecessor=True,
            gate_ids=gate_ids,
            gate_by_id=gate_by_id,
            gate_index=gate_index,
            validation=validation,
        )

    for index, gate_id in enumerate(instantiated[:-1]):
        if gate_id not in packets:
            continue
        manifest, acceptance = packets[gate_id]
        validation.require(acceptance.get("disposition") == "PASS", f"canonical predecessor must be PASS: {gate_id}")
        if acceptance.get("disposition") != "PASS":
            continue
        effect = pass_effect(gate_id, acceptance, gate_ids, gate_by_id, gate_index)
        next_gate_id = instantiated[index + 1]
        same_phase = gate_by_id[gate_id]["phase_id"] == gate_by_id[next_gate_id]["phase_id"]
        expected_effect = "PUBLISH_NEXT_GATE" if same_phase else "WAIT_FOR_NEXT_PHASE_AUTHORITY"
        validation.require(effect == expected_effect, f"accepted transition cannot instantiate {next_gate_id}: {gate_id}")
        if not same_phase and next_gate_id in packets:
            next_manifest = packets[next_gate_id][0]
            next_maturity = next_manifest.get("packet_maturity")
            if next_maturity == "DRAFT":
                reopening_events = [
                    event
                    for event in state.get("invalidations", [])
                    if (
                        isinstance(event, dict)
                        and isinstance(event.get("affected"), list)
                        and event["affected"]
                        and isinstance(event["affected"][0], dict)
                        and event["affected"][0].get("gate_id") == next_gate_id
                    )
                ]
                receipt_digests = {
                    artifact.get("sha256")
                    for artifact in next_manifest.get("artifacts", [])
                    if isinstance(artifact, dict) and is_invalidation_receipt(artifact)
                }
                validation.require(bool(reopening_events), f"initial cross-phase entry cannot be instantiated as DRAFT: {next_gate_id}")
                if reopening_events:
                    validation.require(
                        reopening_events[-1].get("trigger_sha256") in receipt_digests,
                        f"cross-phase DRAFT rerun omits its latest invalidation trigger receipt: {next_gate_id}",
                    )
            else:
                validation.require(
                    next_maturity in {"INPUT_LOCKED", "SEALED"},
                    f"an initial cross-phase gate requires its authority-bearing input lock: {next_gate_id}",
                )

    if last_gate not in packets:
        return
    _, last_acceptance = packets[last_gate]
    disposition = last_acceptance.get("disposition")
    if disposition == "NOT_RUN":
        return
    if disposition in {"PARTIAL", "FAIL", "BLOCKED"}:
        return
    validation.require(disposition == "PASS", "final canonical packet has no derivable execution state")
    if disposition != "PASS":
        return

    effect = pass_effect(last_gate, last_acceptance, gate_ids, gate_by_id, gate_index)
    validation.require(
        effect in {"WAIT_FOR_NEXT_PHASE_AUTHORITY", "TERMINAL_NO_WINNER", "MANDATORY_DAG_COMPLETE"},
        f"PASS at {last_gate} requires publication of its successor",
    )


def validate_history(
    state: dict,
    gate_ids: list[str],
    gate_by_id: dict[str, dict],
    gate_index: dict[str, int],
    validation: Validation,
) -> None:
    invalidations = state.get("invalidations", [])
    if not isinstance(invalidations, list):
        return
    archived_revisions: dict[str, list[int]] = {}
    packet_receipts: dict[tuple[str, int], set[str]] = {}
    available_packets: dict[tuple[str, str, str, str], tuple[Path, dict]] = {}
    archived_manifests: list[tuple[str, dict]] = []
    for event in invalidations:
        if not isinstance(event, dict):
            continue
        for row in event.get("affected", []):
            if not isinstance(row, dict) or row.get("gate_id") not in gate_by_id:
                continue
            archive = archive_path(row)
            if not archive.is_dir():
                continue
            manifest, archive_acceptance = validate_packet(
                archive,
                row["gate_id"],
                live=False,
                resolve_predecessor=False,
                gate_ids=gate_ids,
                gate_by_id=gate_by_id,
                gate_index=gate_index,
                validation=validation,
            )
            label = archive_relative_path(row).as_posix()
            validation.require(row.get("manifest_sha256") == sha256(archive / "manifest.json"), f"archive manifest digest mismatch: {label}")
            validation.require(row.get("acceptance_sha256") == sha256(archive / "acceptance.json"), f"archive acceptance digest mismatch: {label}")
            packet_key = (
                row["gate_id"],
                str(manifest.get("lineage_id")),
                sha256(archive / "manifest.json"),
                sha256(archive / "acceptance.json"),
            )
            validation.require(packet_key not in available_packets, f"duplicate preserved packet identity: {label}")
            available_packets[packet_key] = (archive, archive_acceptance)
            archived_manifests.append((label, manifest))
            receipt_digests = {
                artifact["sha256"]
                for artifact in manifest.get("artifacts", [])
                if isinstance(artifact, dict) and is_invalidation_receipt(artifact)
            }
            lineage = str(manifest.get("lineage_id", ""))
            if LINEAGE.fullmatch(lineage):
                revision = int(lineage.rsplit("-r", 1)[1])
                archived_revisions.setdefault(row["gate_id"], []).append(revision)
                packet_receipts[(row["gate_id"], revision)] = receipt_digests

    instantiated = instantiated_gate_ids(state, gate_ids)
    for gate_id in instantiated:
        if gate_id not in gate_by_id:
            continue
        revisions = archived_revisions.get(gate_id, [])
        canonical_path = packet_path(gate_by_id[gate_id])
        canonical = load_json(canonical_path / "manifest.json", validation)
        canonical_acceptance = load_json(canonical_path / "acceptance.json", validation)
        packet_key = (
            gate_id,
            str(canonical.get("lineage_id")),
            sha256(canonical_path / "manifest.json"),
            sha256(canonical_path / "acceptance.json"),
        )
        validation.require(packet_key not in available_packets, f"canonical packet reuses an archived exact identity: {gate_id}")
        available_packets[packet_key] = (canonical_path, canonical_acceptance)
        receipt_digests = {
            artifact["sha256"]
            for artifact in canonical.get("artifacts", [])
            if isinstance(artifact, dict) and is_invalidation_receipt(artifact)
        }
        lineage = str(canonical.get("lineage_id", ""))
        if LINEAGE.fullmatch(lineage):
            revision = int(lineage.rsplit("-r", 1)[1])
            validation.require(revision == len(revisions) + 1, f"canonical lineage must be the exact next contiguous revision: {gate_id}")
            packet_receipts[(gate_id, revision)] = receipt_digests

    # Recheck the packet identities authenticated by every retained transition,
    # not merely by the current frontier.  A state object is unusable if any
    # historical prior-packet row no longer resolves to one exact canonical or
    # archived byte pair.  Replacement identity is intentionally lineage-only:
    # its packet may mature after state-last publication, whereas it becomes an
    # exact manifest/acceptance pair before a later transition can consume it.
    cursor = state
    cursor_label = "state.json"
    seen_transition_states: set[str] = set()
    for _ in range(65):
        retained_transition = cursor.get("transition")
        if not isinstance(retained_transition, dict):
            break
        retained_prior_rows = retained_transition.get("prior_packets")
        if isinstance(retained_prior_rows, list):
            for position, row in enumerate(retained_prior_rows):
                if not isinstance(row, dict):
                    continue
                identity = (
                    str(row.get("gate_id")),
                    str(row.get("lineage_id")),
                    str(row.get("manifest_sha256")),
                    str(row.get("acceptance_sha256")),
                )
                validation.require(
                    identity in available_packets,
                    f"retained transition prior packet does not resolve to exact preserved bytes: {cursor_label}/{position}",
                )
        retained_replacement = retained_transition.get("replacement")
        if isinstance(retained_replacement, dict):
            replacement_identity = (
                str(retained_replacement.get("gate_id")),
                str(retained_replacement.get("lineage_id")),
            )
            replacements = [
                identity
                for identity in available_packets
                if identity[:2] == replacement_identity
            ]
            validation.require(
                len(replacements) == 1,
                f"retained transition replacement does not resolve to one preserved lineage: {cursor_label}",
            )
        retained_prior_digest = retained_transition.get("prior_state_sha256")
        if not is_digest(retained_prior_digest):
            break
        retained_prior_digest = str(retained_prior_digest)
        if retained_prior_digest in seen_transition_states:
            break
        seen_transition_states.add(retained_prior_digest)
        retained_prior_path = HISTORY_ROOT / "states" / f"{retained_prior_digest}.json"
        if not retained_prior_path.is_file():
            break
        cursor = load_json(retained_prior_path, validation)
        cursor_label = retained_prior_path.relative_to(EXECUTION_ROOT).as_posix()
    else:
        validation.require(False, "retained transition packet-binding chain exceeds 64 transitions")

    transition = state.get("transition")
    if isinstance(transition, dict):
        kind = transition.get("kind")
        replacement = transition.get("replacement")
        replacement_gate = str(replacement.get("gate_id")) if isinstance(replacement, dict) else ""
        replacement_index = gate_index.get(replacement_gate, -1)
        latest_event = invalidations[-1] if kind == "INVALIDATE" and invalidations else None
        latest_rows = latest_event.get("affected", []) if isinstance(latest_event, dict) else []
        latest_archives = {
            str(row.get("gate_id")): row
            for row in latest_rows
            if isinstance(row, dict)
        }
        prior_rows = transition.get("prior_packets")
        if isinstance(prior_rows, list):
            for position, row in enumerate(prior_rows):
                if not isinstance(row, dict) or position >= len(gate_ids):
                    continue
                gate_id = gate_ids[position]
                if kind == "INVALIDATE" and position >= replacement_index:
                    archive_row = latest_archives.get(gate_id)
                    prior_packet_path = archive_path(archive_row) if isinstance(archive_row, dict) else Path("/nonexistent")
                else:
                    prior_packet_path = packet_path(gate_by_id[gate_id])
                validation.require(prior_packet_path.is_dir(), f"authenticated prior packet bytes are missing: {gate_id}")
                if not prior_packet_path.is_dir():
                    continue
                prior_manifest = load_json(prior_packet_path / "manifest.json", validation)
                expected_identity = {
                    "gate_id": gate_id,
                    "lineage_id": prior_manifest.get("lineage_id"),
                    "manifest_sha256": sha256(prior_packet_path / "manifest.json"),
                    "acceptance_sha256": sha256(prior_packet_path / "acceptance.json"),
                }
                validation.require(row == expected_identity, f"authenticated prior packet identity does not match exact retained bytes: {gate_id}")
        if replacement_gate in gate_by_id and isinstance(replacement, dict):
            replacement_manifest = load_json(packet_path(gate_by_id[replacement_gate]) / "manifest.json", validation)
            validation.require(
                replacement.get("lineage_id") == replacement_manifest.get("lineage_id"),
                "execution state replacement lineage differs from the canonical packet",
            )

    for gate_id, revisions in archived_revisions.items():
        validation.require(revisions == list(range(1, len(revisions) + 1)), f"archived lineage revisions must be ordered, unique, and contiguous from r0001 for {gate_id}")

    for label, manifest in archived_manifests:
        for predecessor in manifest.get("predecessors", []):
            if not isinstance(predecessor, dict):
                continue
            edge = (
                str(predecessor.get("gate_id")),
                str(predecessor.get("lineage_id")),
                str(predecessor.get("manifest_sha256")),
                str(predecessor.get("acceptance_sha256")),
            )
            resolved = available_packets.get(edge)
            validation.require(resolved is not None, f"archived predecessor edge does not resolve to preserved exact bytes: {label}")
            if resolved is None:
                continue
            _, predecessor_acceptance = resolved
            validation.require(predecessor_acceptance.get("disposition") == "PASS", f"archived packet consumed a predecessor without independent PASS: {label}")

    for index, event in enumerate(invalidations):
        if not isinstance(event, dict):
            continue
        affected = event.get("affected", [])
        if not isinstance(affected, list) or not affected or not isinstance(affected[0], dict):
            continue
        owner_row = affected[0]
        owner_gate = str(owner_row.get("gate_id"))
        owner_manifest = load_json(archive_path(owner_row) / "manifest.json", validation)
        old_lineage = str(owner_manifest.get("lineage_id", ""))
        if not is_gate_lineage(owner_gate, old_lineage):
            continue
        old_revision = int(old_lineage.rsplit("-r", 1)[1])
        replacement = packet_receipts.get((owner_gate, old_revision + 1))
        validation.require(
            replacement is not None,
            f"invalidation event {index} has no exact-next lineage for its earliest owner",
        )
        if replacement is None:
            continue
        replacement_receipts = replacement
        validation.require(
            event.get("trigger_sha256") in replacement_receipts,
            f"invalidation event {index} trigger is not preserved by the exact-next lineage of its earliest owner",
        )


def collect_authority_records(
    state: dict,
    gate_ids: list[str],
    gate_by_id: dict[str, dict],
    validation: Validation,
) -> list[dict]:
    """Collect canonical and declared archived packets under one exact identity."""
    records: list[dict] = []
    seen: set[tuple[str, str, str, str]] = set()

    def append_record(path: Path, gate_id: str, archived: bool) -> None:
        manifest = load_json(path / "manifest.json", validation)
        acceptance = load_json(path / "acceptance.json", validation)
        identity = (
            gate_id,
            str(manifest.get("lineage_id")),
            sha256(path / "manifest.json"),
            sha256(path / "acceptance.json"),
        )
        validation.require(identity not in seen, f"duplicate authority packet identity: {path}")
        if identity in seen:
            return
        seen.add(identity)
        records.append(
            {
                "path": path,
                "gate_id": gate_id,
                "phase_id": str(manifest.get("phase_id")),
                "manifest": manifest,
                "acceptance": acceptance,
                "identity": identity,
                "archived": archived,
            }
        )

    for gate_id in instantiated_gate_ids(state, gate_ids):
        if gate_id in gate_by_id:
            append_record(packet_path(gate_by_id[gate_id]), gate_id, False)
    for event in state.get("invalidations", []):
        if not isinstance(event, dict):
            continue
        for row in event.get("affected", []):
            if not isinstance(row, dict) or row.get("gate_id") not in gate_by_id:
                continue
            path = archive_path(row)
            if path.is_dir():
                append_record(path, str(row["gate_id"]), True)
    return records


def invalidation_verifier_arguments(
    state: dict,
    records_by_lineage: dict[tuple[str, str], dict],
    validation: Validation,
) -> tuple[str, ...]:
    transition = state.get("transition")
    if not isinstance(transition, dict) or transition.get("kind") != "INVALIDATE":
        return ()
    replacement = transition.get("replacement")
    invalidations = state.get("invalidations")
    validation.require(isinstance(replacement, dict), "INVALIDATE authority replacement missing")
    validation.require(isinstance(invalidations, list) and bool(invalidations), "INVALIDATE authority event missing")
    if not isinstance(replacement, dict) or not isinstance(invalidations, list) or not invalidations:
        return ()
    latest = invalidations[-1]
    affected = latest.get("affected") if isinstance(latest, dict) else None
    trigger = latest.get("trigger_sha256") if isinstance(latest, dict) else None
    validation.require(
        isinstance(affected, list) and bool(affected) and isinstance(affected[0], dict),
        "INVALIDATE authority event has no earliest affected owner",
    )
    validation.require(is_digest(trigger), "INVALIDATE authority trigger digest malformed")
    if not isinstance(affected, list) or not affected or not isinstance(affected[0], dict) or not is_digest(trigger):
        return ()
    owner_gate_id = str(affected[0].get("gate_id", ""))
    replacement_gate_id = str(replacement.get("gate_id", ""))
    replacement_lineage_id = str(replacement.get("lineage_id", ""))
    validation.require(
        replacement_gate_id == owner_gate_id,
        "INVALIDATE authority replacement is not the earliest affected owner",
    )
    record = records_by_lineage.get((replacement_gate_id, replacement_lineage_id))
    validation.require(record is not None, "INVALIDATE authority replacement packet bytes unavailable")
    if record is None:
        return ()
    receipt_rows = [
        row
        for row in record["manifest"].get("artifacts", [])
        if isinstance(row, dict)
        and is_invalidation_receipt(row)
        and row.get("sha256") == trigger
    ]
    validation.require(
        len(receipt_rows) == 1,
        "INVALIDATE authority requires exactly one trigger receipt in the canonical replacement packet",
    )
    if len(receipt_rows) != 1:
        return ()
    receipt_path = record["path"] / str(receipt_rows[0]["path"])
    validation.require(receipt_path.is_file(), "INVALIDATE authority trigger receipt bytes missing")
    if not receipt_path.is_file():
        return ()
    validation.require(
        sha256(receipt_path) == trigger,
        "INVALIDATE authority trigger receipt digest mismatch",
    )
    return (
        "--invalidation-receipt",
        str(receipt_path.resolve()),
        "--invalidation-receipt-sha256",
        str(trigger),
        "--invalidation-owner-gate-id",
        owner_gate_id,
    )


def resolve_phase_entry_record(
    record: dict,
    records_by_identity: dict[tuple[str, str, str, str], dict],
    gate_by_id: dict[str, dict],
    gate_index: dict[str, int],
    validation: Validation,
) -> dict | None:
    """Follow exact predecessor bytes to the first gate of the same phase."""
    phase_id = record["phase_id"]
    phase_gates = sorted(
        (gate_id for gate_id, gate in gate_by_id.items() if gate["phase_id"] == phase_id),
        key=lambda gate_id: gate_index[gate_id],
    )
    if not phase_gates:
        validation.require(False, f"authority chain names unknown phase: {phase_id}")
        return None
    entry_gate_id = phase_gates[0]
    current = record
    visited: set[tuple[str, str, str, str]] = set()
    while current["gate_id"] != entry_gate_id:
        identity = current["identity"]
        validation.require(identity not in visited, f"authority predecessor cycle: {record['gate_id']}")
        if identity in visited:
            return None
        visited.add(identity)
        rows = current["manifest"].get("predecessors")
        validation.require(isinstance(rows, list) and len(rows) == 1, f"same-phase authority chain must have one exact predecessor: {current['gate_id']}")
        if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict):
            return None
        row = rows[0]
        edge = (
            str(row.get("gate_id")),
            str(row.get("lineage_id")),
            str(row.get("manifest_sha256")),
            str(row.get("acceptance_sha256")),
        )
        predecessor = records_by_identity.get(edge)
        validation.require(predecessor is not None, f"authority predecessor bytes are unavailable: {current['gate_id']}")
        if predecessor is None:
            return None
        validation.require(predecessor["phase_id"] == phase_id, f"same-phase authority chain crossed a phase boundary: {current['gate_id']}")
        validation.require(
            gate_index.get(predecessor["gate_id"], -2) + 1 == gate_index.get(current["gate_id"], -1),
            f"authority chain skipped or repeated a gate: {current['gate_id']}",
        )
        validation.require(predecessor["acceptance"].get("disposition") == "PASS", f"authority chain consumed a non-PASS predecessor: {current['gate_id']}")
        if predecessor["phase_id"] != phase_id:
            return None
        current = predecessor
    return current


def phase_authority(
    entry_record: dict,
    gate_by_id: dict[str, dict],
    validation: Validation,
) -> tuple[Path, Path, dict] | None:
    """Resolve the two phase-entry snapshots without adding later-gate pointers."""
    packet = entry_record["path"]
    lock_path = packet / "evidence" / "input-lock.json"
    if not lock_path.is_file():
        validation.require(False, f"phase-entry authority input lock missing: {entry_record['gate_id']}")
        return None
    lock = load_json(lock_path, validation)
    rows = {
        row.get("logical_path"): row
        for row in lock.get("entries", [])
        if isinstance(row, dict) and isinstance(row.get("logical_path"), str)
    }
    phase_id = entry_record["phase_id"]
    receipt_name = f"authority/phase-{phase_id}-authorization.receipt"
    attestation_name = f"authority/phase-{phase_id}-entry-attestation.json"
    receipt_row = rows.get(receipt_name)
    attestation_row = rows.get(attestation_name)
    validation.require(isinstance(receipt_row, dict) and isinstance(attestation_row, dict), f"phase-entry authority snapshot pair missing: {entry_record['gate_id']}")
    if not isinstance(receipt_row, dict) or not isinstance(attestation_row, dict):
        return None
    receipt_path = packet / "evidence" / str(receipt_row.get("snapshot_path"))
    attestation_path = packet / "evidence" / str(attestation_row.get("snapshot_path"))
    if not receipt_path.is_file() or not attestation_path.is_file():
        validation.require(False, f"phase-entry authority snapshot bytes missing: {entry_record['gate_id']}")
        return None
    attestation = validate_phase_entry_attestation(
        attestation_path,
        receipt_path,
        entry_record["manifest"],
        gate_by_id,
        validation,
    )
    return receipt_path, attestation_path, attestation


def actor_has_capability(attestation: dict, principal: tuple[str, str, str] | None, capability: str) -> bool:
    return principal is not None and any(
        principal_tuple(actor) == principal
        and isinstance(actor.get("capabilities"), list)
        and capability in actor["capabilities"]
        for actor in attestation.get("authorized_actors", [])
        if isinstance(actor, dict)
    )


def validity_covers(attestation: dict, timestamp: object) -> bool:
    validity = attestation.get("validity")
    if not isinstance(validity, dict) or not is_timestamp(timestamp):
        return False
    required = ("not_before", "expires_at", "revocation_checked_at")
    if not all(is_timestamp(validity.get(field)) for field in required):
        return False
    parse = lambda value: datetime.strptime(str(value), "%Y-%m-%dT%H:%M:%SZ")
    action_time = parse(timestamp)
    return (
        validity.get("revocation_status") == "GOOD"
        and parse(validity["not_before"]) <= parse(validity["revocation_checked_at"])
        <= action_time < parse(validity["expires_at"])
    )


def authority_record_use(record: dict, active_phase: str | None) -> str:
    """Derive verifier use from the protected artifact's owning packet."""
    return (
        "CURRENT_AUTHORITY"
        if not record["archived"] and record["phase_id"] == active_phase
        else "HISTORICAL_VERIFY_ONLY"
    )


def load_authority_policy(
    config: tuple[Path, str] | None,
    catalog_sha256: str,
    gate_by_id: dict[str, dict],
    validation: Validation,
) -> tuple[dict[tuple[str, str, str, str, str, str], dict], str] | None:
    """Load one externally pinned catalog of exact artifact-to-verifier bindings."""
    if config is None:
        return None
    starting_error_count = len(validation.errors)
    raw_path, expected_digest = config
    validation.require(raw_path.is_absolute(), "authority policy path must be absolute")
    validation.require(Path(os.path.normpath(str(raw_path))) == raw_path, "authority policy path must be lexical and normalized")
    validation.require(is_digest(expected_digest), "authority policy digest malformed")
    try:
        inside_package = os.path.commonpath((str(raw_path), str(PLAN_ROOT))) == str(PLAN_ROOT)
    except ValueError:
        inside_package = True
    validation.require(not inside_package, "authority policy must remain outside the mutable plan package")

    policy: dict = {}
    policy_digest = ""
    policy_fd = -1
    try:
        policy_fd = open_absolute_nofollow(raw_path)
        policy_bytes = read_stable_regular_fd(policy_fd, 8 * 1024 * 1024)
        policy_digest = hashlib.sha256(policy_bytes).hexdigest()
        validation.require(policy_digest == expected_digest, "authority policy raw-byte digest mismatch")
        decoded = policy_bytes.decode("utf-8")
        parsed = decode_json(decoded)
        validation.require(isinstance(parsed, dict), "authority policy JSON root must be an object")
        if isinstance(parsed, dict):
            policy = parsed
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, DuplicateJsonMemberError) as exc:
        validation.require(False, f"cannot read exact authority policy object: {exc}")
    finally:
        if policy_fd >= 0:
            os.close(policy_fd)

    validation.require(set(policy) == AUTHORITY_POLICY_KEYS, "authority policy field set drift")
    validation.require(policy.get("policy_version") == 3, "authority policy version drift")
    validation.require(policy.get("catalog_sha256") == catalog_sha256, "authority policy catalog binding drift")
    bindings = policy.get("bindings")
    validation.require(isinstance(bindings, list) and bool(bindings), "authority policy bindings missing")
    index: dict[tuple[str, str, str, str, str, str], dict] = {}
    ordered_keys: list[tuple[str, str, str, str, str, str]] = []
    if isinstance(bindings, list):
        for position, binding in enumerate(bindings):
            valid_binding = isinstance(binding, dict) and set(binding) == AUTHORITY_BINDING_KEYS
            validation.require(valid_binding, f"authority policy binding {position} malformed")
            if not valid_binding:
                continue
            key = binding.get("key")
            verifier = binding.get("verifier")
            validation.require(isinstance(key, dict) and set(key) == AUTHORITY_LOOKUP_KEYS, f"authority lookup key {position} malformed")
            validation.require(isinstance(verifier, dict) and set(verifier) == AUTHORITY_VERIFIER_KEYS, f"authority verifier {position} malformed")
            if not isinstance(key, dict) or not isinstance(verifier, dict):
                continue
            lookup = authority_lookup_tuple(key)
            ordered_keys.append(lookup)
            validation.require(lookup not in index, f"duplicate authority lookup key at binding {position}")
            if lookup not in index:
                index[lookup] = binding
            validation.require(key.get("kind") in AUTHORITY_ARTIFACT_KINDS, f"authority artifact kind invalid at binding {position}")
            gate_id = str(key.get("gate_id"))
            validation.require(gate_id in gate_by_id, f"authority binding names unknown gate at binding {position}")
            if gate_id in gate_by_id:
                validation.require(key.get("phase_id") == gate_by_id[gate_id]["phase_id"], f"authority binding phase mismatch at binding {position}")
            validation.require(is_gate_lineage(gate_id, key.get("lineage_id")), f"authority binding lineage malformed at binding {position}")
            validation.require(is_digest(key.get("artifact_sha256")) and is_digest(key.get("bound_sha256")), f"authority binding digest malformed at binding {position}")
            validation.require(binding.get("use") in AUTHORITY_USES, f"authority binding use invalid at binding {position}")
            validate_principal(verifier, AUTHORITY_VERIFIER_KEYS, f"authority verifier {position}", validation)
            executable = Path(str(verifier.get("executable", "")))
            validation.require(executable.is_absolute(), f"authority verifier executable must be absolute at binding {position}")
            validation.require(Path(os.path.normpath(str(executable))) == executable, f"authority verifier executable path must be lexical and normalized at binding {position}")
            validation.require(is_digest(verifier.get("build_sha256")), f"authority verifier build digest malformed at binding {position}")
            validation.require(is_digest(verifier.get("trust_root_sha256")), f"authority verifier trust-root digest malformed at binding {position}")
    validation.require(ordered_keys == sorted(ordered_keys), "authority policy bindings must be sorted by exact lookup key")
    # A policy error is a dispatch barrier, not merely a diagnostic.  In
    # particular, never execute a verifier selected by bytes whose path,
    # digest, catalog binding, shape, identity, or ordering failed validation.
    if len(validation.errors) != starting_error_count:
        return None
    return index, policy_digest


def verify_authority_artifact(
    policy_state: tuple[dict[tuple[str, str, str, str, str, str], dict], str] | None,
    key: dict,
    expected_use: str,
    artifact_path: Path,
    bound_path: Path,
    independent_from: list[tuple[str, str, str] | None],
    catalog_sha256: str,
    validation: Validation,
    additional_arguments: tuple[str, ...] = (),
) -> None:
    """Seal, hash, and execute one clone of a retained verifier source object."""
    # Local/package checks and earlier authority checks are prerequisites for
    # code execution.  Stop at the first failure so an invalid later binding
    # cannot launch merely because Validation aggregates diagnostics.
    if validation.errors:
        return
    if policy_state is None:
        validation.require(False, f"authority policy required for protected artifact: {artifact_path}")
        return
    index, policy_sha256 = policy_state
    lookup = authority_lookup_tuple(key)
    binding = index.get(lookup)
    validation.require(binding is not None, f"authority policy has no exact binding: {lookup}")
    if binding is None:
        return
    validation.require(binding.get("use") == expected_use, f"authority binding use drift: {lookup}")
    verifier = binding.get("verifier")
    if not isinstance(verifier, dict):
        return
    verifier_principal = principal_tuple(verifier)
    validation.require(
        principals_are_axis_independent(verifier_principal, *independent_from),
        f"authority verifier is not independent on all three axes: {lookup}",
    )
    executable = Path(str(verifier.get("executable")))
    mode = {
        "CURRENT_AUTHORITY": "current-authority",
        "HISTORICAL_VERIFY_ONLY": "historical-verification",
        "ONE_SHOT_STATE_COMMIT": "one-shot-state-commit",
    }.get(expected_use)
    validation.require(mode is not None, f"unsupported authority use at dispatch: {expected_use}")
    if mode is None or validation.errors:
        return
    command = [
        "ephemeral-authority-verifier",
        "--mode",
        mode,
        "--artifact-kind",
        str(key["kind"]),
        "--artifact",
        str(artifact_path.resolve()),
        "--bound-artifact",
        str(bound_path.resolve()),
        "--catalog-sha256",
        catalog_sha256,
        "--phase-id",
        str(key["phase_id"]),
        "--gate-id",
        str(key["gate_id"]),
        "--lineage-id",
        str(key["lineage_id"]),
        "--artifact-sha256",
        str(key["artifact_sha256"]),
        "--bound-sha256",
        str(key["bound_sha256"]),
        "--trust-root-sha256",
        str(verifier.get("trust_root_sha256")),
        "--policy-sha256",
        policy_sha256,
        *additional_arguments,
    ]
    if not sealed_fd_exec_supported():
        validation.require(
            False,
            f"authority verification requires Linux sealed exact-fd execution; no fallback is permitted: {lookup}",
        )
        return
    if not verifier_process_limit_is_enforceable():
        validation.require(
            False,
            "authority verification requires nonzero real/effective/saved UIDs and empty "
            f"inherited/permitted/effective/ambient capability sets: {lookup}",
        )
        return

    source_fd = -1
    sealed_fd = -1
    try:
        source_fd = open_absolute_nofollow(executable)
        sealed_fd = clone_to_sealed_executable_fd(source_fd)
        os.close(source_fd)
        source_fd = -1
        observed_build = hash_stable_executable_fd(sealed_fd)
        validation.require(
            observed_build == verifier.get("build_sha256"),
            f"authority verifier sealed-clone build digest mismatch: {lookup}",
        )
        if observed_build != verifier.get("build_sha256"):
            return
        returncode, stdout, stderr, dispatch_error = run_sealed_exact_fd(
            sealed_fd,
            command,
            timeout_seconds=30.0,
            output_limit=64 * 1024,
        )
    except OSError as exc:
        validation.require(False, f"authority verifier open/clone/seal/hash failed for {lookup}: {exc}")
        return
    finally:
        if source_fd >= 0:
            os.close(source_fd)
        if sealed_fd >= 0:
            os.close(sealed_fd)

    validation.require(dispatch_error is None, f"authority verifier dispatch failed for {lookup}: {dispatch_error}")
    validation.require(returncode == 0, f"authority verifier rejected {lookup} with exit {returncode}")
    validation.require(stdout == b"PASS\n", f"authority verifier stdout contract drift: {lookup}")
    validation.require(stderr == b"", f"authority verifier emitted stderr: {lookup}")


def validate_execution_authority(
    state: dict,
    gate_ids: list[str],
    gate_by_id: dict[str, dict],
    gate_index: dict[str, int],
    policy_config: tuple[Path, str] | None,
    validation: Validation,
) -> None:
    """Authenticate production, acceptance, and transitive phase authority."""
    records = collect_authority_records(state, gate_ids, gate_by_id, validation)
    records_by_identity = {record["identity"]: record for record in records}
    records_by_lineage: dict[tuple[str, str], dict] = {}
    for record in records:
        lineage_key = (record["gate_id"], str(record["manifest"].get("lineage_id")))
        validation.require(lineage_key not in records_by_lineage, f"duplicate authority packet lineage: {lineage_key}")
        if lineage_key not in records_by_lineage:
            records_by_lineage[lineage_key] = record
    protected = [
        record
        for record in records
        if record["manifest"].get("packet_maturity") in {"INPUT_LOCKED", "SEALED"}
        or record["acceptance"].get("disposition") != "NOT_RUN"
    ]
    state_transition = state.get("transition")
    # All non-executable structural, semantic, filesystem, and package-seal
    # checks run before this function.  Any failure makes external dispatch
    # unsafe and unnecessary; the existing diagnostics remain authoritative.
    if validation.errors:
        return
    validation.require(
        (not protected and state_transition is None) or policy_config is not None,
        "protected artifacts and non-bootstrap state transitions require an externally pinned authority policy",
    )
    policy_state = load_authority_policy(
        policy_config,
        sha256(EXECUTION_ROOT / "gates.json"),
        gate_by_id,
        validation,
    )

    canonical = sorted(
        (record for record in records if not record["archived"]),
        key=lambda record: gate_index[record["gate_id"]],
    )
    active_phase = (
        canonical[-1]["phase_id"]
        if canonical and canonical[-1]["acceptance"].get("disposition") == "NOT_RUN"
        else None
    )
    phase_uses: dict[tuple[str, str], str] = {}
    for record in protected:
        record_use = authority_record_use(record, active_phase)
        entry_record = resolve_phase_entry_record(
            record,
            records_by_identity,
            gate_by_id,
            gate_index,
            validation,
        )
        if entry_record is None:
            continue
        resolved = phase_authority(entry_record, gate_by_id, validation)
        if resolved is None:
            continue
        receipt_path, attestation_path, attestation = resolved
        entry_use = authority_record_use(entry_record, active_phase)
        phase_key = (sha256(attestation_path), sha256(receipt_path))
        prior_use = phase_uses.setdefault(phase_key, entry_use)
        validation.require(prior_use == entry_use, f"one phase-entry attestation cannot be both current and historical: {record['gate_id']}")

        actors = [
            principal_tuple(actor)
            for actor in attestation.get("authorized_actors", [])
            if isinstance(actor, dict)
        ]
        authorizer = principal_tuple(attestation.get("authorizer"))
        phase_policy_key = {
            "kind": "phase-entry-attestation",
            "phase_id": entry_record["phase_id"],
            "gate_id": entry_record["gate_id"],
            "lineage_id": entry_record["manifest"].get("lineage_id"),
            "artifact_sha256": sha256(attestation_path),
            "bound_sha256": sha256(receipt_path),
        }
        verify_authority_artifact(
            policy_state,
            phase_policy_key,
            entry_use,
            attestation_path,
            receipt_path,
            [authorizer, *actors],
            str(entry_record["manifest"].get("catalog_sha256")),
            validation,
        )

        packet = record["path"]
        lock_path = packet / "evidence" / "input-lock.json"
        lock = load_json(lock_path, validation)
        producer = principal_tuple(lock.get("producer"))
        validation.require(
            actor_has_capability(attestation, producer, f"produce:{record['gate_id']}"),
            f"input-lock producer lacks exact phase capability: {record['gate_id']}",
        )
        validation.require(validity_covers(attestation, lock.get("locked_at")), f"input lock lies outside valid phase authority: {record['gate_id']}")
        lock_key = {
            "kind": "input-lock",
            "phase_id": record["phase_id"],
            "gate_id": record["gate_id"],
            "lineage_id": record["manifest"].get("lineage_id"),
            "artifact_sha256": sha256(lock_path),
            "bound_sha256": sha256(attestation_path),
        }
        verify_authority_artifact(
            policy_state,
            lock_key,
            record_use,
            lock_path,
            attestation_path,
            [producer, authorizer],
            str(record["manifest"].get("catalog_sha256")),
            validation,
        )

        acceptance = record["acceptance"]
        disposition = acceptance.get("disposition")
        acceptor = (
            principal_tuple(acceptance.get("accepted_by"))
            if disposition != "NOT_RUN"
            else None
        )
        result_producer = principal_tuple(record["manifest"].get("producer"))
        manifest_path = packet / "manifest.json"
        if record["manifest"].get("packet_maturity") == "SEALED":
            validation.require(
                result_producer == producer and result_producer is not None,
                f"manifest result producer differs from input-lock producer: {record['gate_id']}",
            )
            validation.require(
                actor_has_capability(attestation, result_producer, f"produce:{record['gate_id']}"),
                f"manifest result producer lacks exact phase capability: {record['gate_id']}",
            )
            validation.require(
                validity_covers(attestation, record["manifest"].get("generated_at")),
                f"manifest production lies outside valid phase authority: {record['gate_id']}",
            )
            manifest_key = {
                "kind": "manifest",
                "phase_id": record["phase_id"],
                "gate_id": record["gate_id"],
                "lineage_id": record["manifest"].get("lineage_id"),
                "artifact_sha256": sha256(manifest_path),
                "bound_sha256": sha256(lock_path),
            }
            manifest_independent_from = [result_producer, authorizer]
            if disposition != "NOT_RUN":
                # A final verdict must have a valid acceptor and the manifest
                # verifier must be independent from it too.  In the legal
                # SEALED / NOT_RUN interval no acceptor exists yet, so a null
                # placeholder must not make producer-seal verification
                # impossible.
                manifest_independent_from.append(acceptor)
            verify_authority_artifact(
                policy_state,
                manifest_key,
                record_use,
                manifest_path,
                lock_path,
                manifest_independent_from,
                str(record["manifest"].get("catalog_sha256")),
                validation,
            )

        # SEALED / NOT_RUN is the legal interval between the authenticated
        # producer seal and the later independent verdict.  The manifest above
        # is protected immediately; no acceptance authority exists yet.
        if disposition == "NOT_RUN":
            continue
        validation.require(
            actor_has_capability(attestation, acceptor, f"accept:{record['gate_id']}"),
            f"acceptor lacks exact phase capability: {record['gate_id']}",
        )
        validation.require(validity_covers(attestation, acceptance.get("accepted_at")), f"acceptance lies outside valid phase authority: {record['gate_id']}")
        validation.require(
            principals_are_axis_independent(producer, acceptor),
            f"producer and acceptor must differ on principal, credential, and control-domain axes: {record['gate_id']}",
        )
        acceptance_path = packet / "acceptance.json"
        acceptance_key = {
            "kind": "acceptance",
            "phase_id": record["phase_id"],
            "gate_id": record["gate_id"],
            "lineage_id": record["manifest"].get("lineage_id"),
            "artifact_sha256": sha256(acceptance_path),
            "bound_sha256": sha256(manifest_path),
        }
        verify_authority_artifact(
            policy_state,
            acceptance_key,
            record_use,
            acceptance_path,
            manifest_path,
            [producer, acceptor, authorizer],
            str(record["manifest"].get("catalog_sha256")),
            validation,
        )

    state_path = EXECUTION_ROOT / "state.json"
    cursor = state
    seen_state_objects: set[str] = set()
    for _ in range(65):
        transition = cursor.get("transition")
        if not isinstance(transition, dict):
            break
        replacement = transition.get("replacement")
        publication = transition.get("publication")
        if not isinstance(replacement, dict) or not isinstance(publication, dict):
            break
        prior_digest = transition.get("prior_state_sha256")
        if not is_digest(prior_digest) or str(prior_digest) in seen_state_objects:
            break
        seen_state_objects.add(str(prior_digest))
        prior_state_path = HISTORY_ROOT / "states" / f"{prior_digest}.json"
        publisher = principal_tuple(transition.get("published_by"))
        commit_authority = principal_tuple(publication.get("authority"))
        gate_id = str(replacement.get("gate_id", ""))
        state_key = {
            "kind": "execution-state",
            "phase_id": gate_by_id.get(gate_id, {}).get("phase_id"),
            "gate_id": replacement.get("gate_id"),
            "lineage_id": replacement.get("lineage_id"),
            "artifact_sha256": sha256(state_path),
            "bound_sha256": str(prior_digest),
        }
        invalidation_arguments = invalidation_verifier_arguments(
            cursor,
            records_by_lineage,
            validation,
        )
        verify_authority_artifact(
            policy_state,
            state_key,
            "ONE_SHOT_STATE_COMMIT",
            state_path,
            prior_state_path,
            [publisher, commit_authority],
            str(cursor.get("catalog_sha256")),
            validation,
            invalidation_arguments,
        )
        if not prior_state_path.is_file():
            break
        cursor = load_json(prior_state_path, validation)
        state_path = prior_state_path
    else:
        validation.require(False, "execution state authority chain exceeds 64 transitions")


def validate_text_files(validation: Validation) -> None:
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    forbidden_directories = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache", "node_modules"}
    forbidden_files = {".DS_Store"}
    for path in sorted(PLAN_ROOT.rglob("*")):
        relative = path.relative_to(PLAN_ROOT)
        if path.is_symlink():
            validation.require(False, f"symlinks are forbidden in the plan package: {relative}")
            continue
        is_directory = path.is_dir()
        is_regular_file = path.is_file()
        validation.require(is_directory or is_regular_file, f"non-regular package entry is forbidden: {relative}")
        if not is_directory and not is_regular_file:
            continue
        validation.require(not (is_directory and path.name in forbidden_directories), f"cache/build directory is forbidden in the plan package: {relative}")
        if is_directory:
            validation.require(any(path.iterdir()), f"empty placeholder directory is forbidden in the plan package: {relative}")
            continue
        validation.require(path.name not in forbidden_files and path.suffix not in {".pyc", ".pyo", ".swp", ".tmp", ".bak", ".orig", ".rej"} and not path.name.endswith("~"), f"cache/temporary file is forbidden in the plan package: {relative}")
        validation.require(path.stat().st_size > 0, f"empty package file: {relative}")
        in_evidence = "evidence" in relative.parts
        if path.suffix not in {".md", ".json", ".py"} and not in_evidence:
            validation.require(False, f"unexpected package file type: {relative}")
            continue
        if path.suffix not in {".md", ".json", ".py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            validation.require(False, f"invalid UTF-8 in {relative}: {exc}")
            continue
        validation.require("\t" not in text, f"tab found in text file: {relative}")
        validation.require(all(line == line.rstrip() for line in text.splitlines()), f"trailing whitespace in text file: {relative}")
        if path.suffix != ".md":
            continue
        fence_count = sum(1 for line in text.splitlines() if line.startswith("```"))
        validation.require(fence_count % 2 == 0, f"unbalanced fenced blocks in Markdown: {relative}")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = target.split(" ", 1)[0]
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = unquote(target.split("#", 1)[0])
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            validation.require(resolved.exists(), f"missing local Markdown target from {relative}: {target_path}")


def validate_package_manifest(validation: Validation) -> None:
    manifest_path = PLAN_ROOT / "evidence" / "draft-manifest.md"
    text = manifest_path.read_text(encoding="utf-8")
    match = re.search(r"<!-- manifest:begin -->\s*```text\n(.*?)\n```\s*<!-- manifest:end -->", text, re.DOTALL)
    validation.require(match is not None, "draft manifest fenced payload missing")
    if match is None:
        return
    rows: dict[str, str] = {}
    for line in match.group(1).splitlines():
        parsed = MANIFEST_LINE.fullmatch(line)
        validation.require(parsed is not None, f"malformed draft-manifest row: {line}")
        if parsed is None:
            continue
        digest, path = parsed.groups()
        validation.require(path not in rows, f"duplicate draft-manifest path: {path}")
        rows[path] = digest

    expected = regular_files(PLAN_ROOT) - {"evidence/draft-manifest.md"}
    validation.require(set(rows) == expected, f"draft-manifest coverage drift; missing={sorted(expected - set(rows))}, extra={sorted(set(rows) - expected)}")
    for path, digest in rows.items():
        target = PLAN_ROOT / path
        if target.is_file():
            validation.require(sha256(target) == digest, f"draft-manifest digest mismatch: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--authority-verifier-policy", type=Path)
    parser.add_argument("--authority-verifier-policy-sha256")
    parser.add_argument("--self-test-authority-fd-exec", action="store_true")
    arguments = parser.parse_args()

    if arguments.self_test_authority_fd_exec:
        self_test_authority_fd_exec()
        return

    validation = Validation()
    policy_values = (
        arguments.authority_verifier_policy,
        arguments.authority_verifier_policy_sha256,
    )
    supplied_policy_values = sum(value is not None for value in policy_values)
    validation.require(
        supplied_policy_values in {0, 2},
        "authority policy path and raw-byte digest must be supplied together",
    )
    policy_config: tuple[Path, str] | None = None
    if supplied_policy_values == 2:
        policy_config = (
            arguments.authority_verifier_policy,
            str(arguments.authority_verifier_policy_sha256),
        )

    validation.require(Path.cwd().resolve() == PLAN_ROOT, f"run from plan root: {PLAN_ROOT}")
    validate_json_parser_contract(validation)
    validate_authority_guard_contract(validation)
    validate_schema_files(validation)
    _, gates, phase_ids, gate_ids, gate_by_id, gate_index = validate_catalog(validation)
    state = validate_state(validation, gate_ids, gate_by_id, gate_index)
    validate_packet_layout(state, gates, phase_ids, gate_ids, gate_by_id, validation)
    validate_template(gate_by_id, validation)
    validate_canonical_packets(state, gate_ids, gate_by_id, gate_index, validation)
    validate_history(state, gate_ids, gate_by_id, gate_index, validation)
    validate_text_files(validation)
    validate_package_manifest(validation)
    validate_execution_authority(
        state,
        gate_ids,
        gate_by_id,
        gate_index,
        policy_config,
        validation,
    )
    validation.finish()


if __name__ == "__main__":
    main()
