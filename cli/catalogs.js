(() => {
  "use strict";

  const operation = (usage, examples, bindings = {}) => ({ usage, examples, bindings });

  window.CLI_CATALOGS = {
    management: {
      binary: "sandbox-manager-cli",
      eyebrow: "Fleet control",
      scope: "System-scoped operations",
      guidance: [
        "Use Management for host discovery, sandbox lifecycle, layer-stack compaction, and exporting published changes.",
        "Operation flags follow the operation name. --gateway-socket, --gateway-auth-token, and --progress are global flags.",
        "The repository wrapper loads the gateway token automatically. Add the repo bin directory to PATH before using the short command name.",
        "Use --progress before any operation to stream progress on stderr; create_sandbox also accepts it after the operation name."
      ],
      operations: {
        create_sandbox: operation(
          "sandbox-manager-cli create_sandbox --image IMAGE --workspace-bind-root PATH [--count N]",
          [
            "sandbox-manager-cli create_sandbox --image ubuntu:24.04 --workspace-bind-root /testbed",
            "sandbox-manager-cli create_sandbox --image ubuntu:24.04 --workspace-bind-root /testbed --count 5"
          ],
          { workspace_root: "--workspace-bind-root PATH" }
        ),
        list_docker_images: operation("sandbox-manager-cli list_docker_images", ["sandbox-manager-cli list_docker_images"]),
        list_workspace_directories: operation(
          "sandbox-manager-cli list_workspace_directories [--path PATH]",
          [
            "sandbox-manager-cli list_workspace_directories",
            "sandbox-manager-cli list_workspace_directories --path /home/me/project"
          ]
        ),
        destroy_sandbox: operation("sandbox-manager-cli destroy_sandbox --sandbox-id ID", ["sandbox-manager-cli destroy_sandbox --sandbox-id sbox-1"]),
        list_sandboxes: operation("sandbox-manager-cli list_sandboxes", ["sandbox-manager-cli list_sandboxes"]),
        inspect_sandbox: operation("sandbox-manager-cli inspect_sandbox --sandbox-id ID", ["sandbox-manager-cli inspect_sandbox --sandbox-id sbox-1"]),
        squash_layerstacks: operation("sandbox-manager-cli squash_layerstacks --sandbox-id ID", ["sandbox-manager-cli squash_layerstacks --sandbox-id sbox-1"]),
        export_changes: operation(
          "sandbox-manager-cli export_changes --sandbox-id ID --dest PATH [--format dir|tar|tar-zst]",
          [
            "sandbox-manager-cli export_changes --sandbox-id sbox-1 --dest /home/me/myproject",
            "sandbox-manager-cli export_changes --sandbox-id sbox-1 --dest /tmp/delta.tar.zst --format tar-zst"
          ]
        )
      }
    },
    runtime: {
      binary: "sandbox-runtime-cli",
      eyebrow: "Inside a sandbox",
      scope: "One required sandbox scope",
      guidance: [
        "Every Runtime operation requires the global --sandbox-id ID selector before the operation name; there is no environment fallback.",
        "Use exec_command without --workspace-session-id for an automatic session that publishes changes when its final command completes.",
        "A running command returns command_session_id. Use it with read_command_lines or write_command_stdin.",
        "File reads target the published snapshot by default; a workspace session id targets that live session instead."
      ],
      operations: {
        exec_command: operation(
          "sandbox-runtime-cli --sandbox-id ID exec_command [--workspace-session-id ID] [--timeout-ms N] [--yield-time-ms N] COMMAND",
          [
            "sandbox-runtime-cli --sandbox-id ID exec_command pwd",
            "sandbox-runtime-cli --sandbox-id ID exec_command --workspace-session-id ws-1 pwd",
            "sandbox-runtime-cli --sandbox-id ID exec_command --workspace-session-id ws-1 --yield-time-ms 0 \"sleep 30\""
          ],
          { sandbox_id: "--sandbox-id ID (global)", cmd: "COMMAND" }
        ),
        write_command_stdin: operation(
          "sandbox-runtime-cli --sandbox-id ID write_command_stdin --command-session-id ID [--yield-time-ms N] TEXT",
          ["sandbox-runtime-cli --sandbox-id ID write_command_stdin --command-session-id cmd-1 hello"],
          { sandbox_id: "--sandbox-id ID (global)", stdin: "TEXT" }
        ),
        read_command_lines: operation(
          "sandbox-runtime-cli --sandbox-id ID read_command_lines --command-session-id ID [--start-offset N] [--limit N]",
          ["sandbox-runtime-cli --sandbox-id ID read_command_lines --command-session-id cmd-1 --start-offset 0 --limit 100"],
          { sandbox_id: "--sandbox-id ID (global)" }
        ),
        file_read: operation(
          "sandbox-runtime-cli --sandbox-id ID file_read --path FILE [--offset N] [--limit N] [--workspace-session-id ID]",
          [
            "sandbox-runtime-cli --sandbox-id ID file_read --path README.md",
            "sandbox-runtime-cli --sandbox-id ID file_read --path src/main.rs --offset 20 --limit 40",
            "sandbox-runtime-cli --sandbox-id ID file_read --path src/main.rs --workspace-session-id ws-1"
          ],
          { sandbox_id: "--sandbox-id ID (global)" }
        ),
        file_write: operation(
          "sandbox-runtime-cli --sandbox-id ID file_write --path FILE --content TEXT [--workspace-session-id ID]",
          [
            "sandbox-runtime-cli --sandbox-id ID file_write --path notes.txt --content 'hello'",
            "sandbox-runtime-cli --sandbox-id ID file_write --path notes.txt --content 'hello' --workspace-session-id ws-1"
          ],
          { sandbox_id: "--sandbox-id ID (global)" }
        ),
        file_edit: operation(
          "sandbox-runtime-cli --sandbox-id ID file_edit --path FILE --edits JSON [--workspace-session-id ID]",
          [
            "sandbox-runtime-cli --sandbox-id ID file_edit --path notes.txt --edits '[{\"old_string\":\"a\",\"new_string\":\"b\"}]'",
            "sandbox-runtime-cli --sandbox-id ID file_edit --path notes.txt --edits '[{\"old_string\":\"a\",\"new_string\":\"b\",\"replace_all\":true}]' --workspace-session-id ws-1"
          ],
          { sandbox_id: "--sandbox-id ID (global)" }
        ),
        file_blame: operation(
          "sandbox-runtime-cli --sandbox-id ID file_blame --path FILE",
          ["sandbox-runtime-cli --sandbox-id ID file_blame --path README.md"],
          { sandbox_id: "--sandbox-id ID (global)" }
        )
      }
    },
    observability: {
      binary: "sandbox-observability-cli",
      eyebrow: "Read-only evidence",
      scope: "System or sandbox scope",
      guidance: [
        "All Observability operations are read-only.",
        "snapshot may omit --sandbox-id to aggregate ready manager-known sandboxes; every other operation requires it.",
        "Operation flags, including --sandbox-id, follow the operation name.",
        "Use trace --trace-id last for the most recent root trace and bounded windows for resource queries."
      ],
      operations: {
        snapshot: operation(
          "sandbox-observability-cli snapshot [--sandbox-id ID]",
          [
            "sandbox-observability-cli snapshot",
            "sandbox-observability-cli snapshot --sandbox-id eos-abc"
          ]
        ),
        trace: operation(
          "sandbox-observability-cli trace --sandbox-id ID [--trace-id TRACE|last]",
          [
            "sandbox-observability-cli trace --sandbox-id eos-abc --trace-id req-7f3",
            "sandbox-observability-cli trace --sandbox-id eos-abc --trace-id last"
          ]
        ),
        events: operation(
          "sandbox-observability-cli events --sandbox-id ID [--name NAME] [--since-ms MS] [--last-n N]",
          [
            "sandbox-observability-cli events --sandbox-id eos-abc",
            "sandbox-observability-cli events --sandbox-id eos-abc --name lease.acquired",
            "sandbox-observability-cli events --sandbox-id eos-abc --last-n 20"
          ]
        ),
        cgroup: operation(
          "sandbox-observability-cli cgroup --sandbox-id ID [--scope SCOPE] [--window-ms MS]",
          [
            "sandbox-observability-cli cgroup --sandbox-id eos-abc",
            "sandbox-observability-cli cgroup --sandbox-id eos-abc --scope ws-1 --window-ms 60000"
          ]
        ),
        layerstack: operation(
          "sandbox-observability-cli layerstack --sandbox-id ID [--workspace-id WS] [--window-ms MS]",
          [
            "sandbox-observability-cli layerstack --sandbox-id eos-abc",
            "sandbox-observability-cli layerstack --sandbox-id eos-abc --workspace-id ws-7"
          ]
        )
      }
    }
  };
})();

