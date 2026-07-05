import subprocess
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class GitManager:
    """Manages Git operations for state management and rollback."""

    @staticmethod
    def run_command(cmd: str) -> Tuple[bool, str, str]:
        """Runs a shell command and returns (success, stdout, stderr)."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            logger.error(f"Error running command '{cmd}': {e}")
            return False, "", str(e)

    @classmethod
    def checkout_branch(cls, branch_name: str, create: bool = False) -> bool:
        """Checks out a git branch."""
        cmd = f"git checkout -b {branch_name}" if create else f"git checkout {branch_name}"
        success, out, err = cls.run_command(cmd)
        if not success:
            logger.error(f"Failed to checkout branch {branch_name}: {err}")
        return success

    @classmethod
    def stash_changes(cls) -> bool:
        """Stashes current changes."""
        success, out, err = cls.run_command("git stash")
        return success

    @classmethod
    def merge_branch(cls, source_branch: str) -> bool:
        """Merges a branch into the current branch."""
        success, out, err = cls.run_command(f"git merge {source_branch}")
        if not success:
            logger.error(f"Failed to merge {source_branch}: {err}")
        return success

    @classmethod
    def delete_branch(cls, branch_name: str, force: bool = True) -> bool:
        """Deletes a branch."""
        flag = "-D" if force else "-d"
        success, out, err = cls.run_command(f"git branch {flag} {branch_name}")
        if not success:
            logger.error(f"Failed to delete branch {branch_name}: {err}")
        return success

    @classmethod
    def rollback(cls, temp_branch: str, main_branch: str = "main") -> bool:
        """Rolls back changes by switching to main and deleting the temp branch."""
        cls.run_command(f"git checkout {main_branch}")
        return cls.delete_branch(temp_branch, force=True)

    @classmethod
    def ensure_clean_state(cls, target_branch: str = "main", temp_branch_prefix: str = "auto-improve") -> bool:
        """
        Pre-flight Hook: Ensures the repository is clean and on the target branch.
        If stuck on a temp branch, it aggressively sanitizes and rolls back.
        """
        success, current_branch, _ = cls.run_command("git rev-parse --abbrev-ref HEAD")
        if not success:
            logger.error("Failed to determine current git branch. Is this a git repository?")
            return False
            
        if temp_branch_prefix in current_branch:
            logger.warning(f"Detected stuck on temp branch '{current_branch}'. Initiating Ironclad Safeguard cleanup...")
            # Aggressive cleanup: hard reset, clean untracked files, checkout target, delete temp
            cls.run_command("git reset --hard")
            cls.run_command("git clean -fd")
            cls.run_command(f"git checkout {target_branch}")
            cls.delete_branch(current_branch, force=True)
            
            # Verify we are on target branch now
            _, new_branch, _ = cls.run_command("git rev-parse --abbrev-ref HEAD")
            if new_branch != target_branch:
                logger.error(f"Critical System Error: Failed to return to '{target_branch}'.")
                return False
            logger.info("Ironclad Safeguard successfully restored repository state.")
            
        return True
