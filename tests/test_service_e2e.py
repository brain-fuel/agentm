import subprocess
import sys


def test_service_cli_reports_status():
    """End-to-end expectation for the AgentM service executable."""
    result = subprocess.run(
        [sys.executable, "-m", "agentm_service", "--status"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "AgentM service" in result.stdout
