import unittest
from unittest.mock import patch
import os
import shutil
import argparse
from src import manage_rules  # Assuming manage_rules.py is in the src directory

class TestManageRules(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = "test_target_repo"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Remove the temporary directory after testing
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch("src.manage_rules.shutil.copytree")
    @patch("src.manage_rules.handle_sync")
    def test_handle_install(self, mock_handle_sync, mock_copytree):
        # Mock command line arguments
        args = argparse.Namespace(
            target_repo_path=self.test_dir,
            template_name="light-spec",
            source_of_truth_dir_name="project_rules_template"
        )
        target_repo_abs_path = os.path.abspath(self.test_dir)

        # Call the handle_install function
        manage_rules.handle_install(args)

        # Assert that shutil.copytree was called with the correct arguments
        mock_copytree.assert_called_once_with(
            os.path.join(manage_rules.ROOT_DIR, manage_rules.TEMPLATE_DIR),
            os.path.join(target_repo_abs_path, "project_rules_template")
        )

        # Assert that handle_sync was called
        mock_handle_sync.assert_called_once_with(args)

    @patch("src.manage_rules.os.path.exists")
    @patch("src.manage_rules.shutil.rmtree")
    @patch("src.manage_rules.os.remove")
    @patch("src.manage_rules.copy_and_number_files")
    @patch("src.manage_rules.copy_and_restructure_roocode")
    @patch("src.manage_rules.concatenate_ordered_files")
    def test_handle_sync(self, mock_concatenate, mock_roocode, mock_number_files, mock_remove, mock_rmtree, mock_exists):
        # Set up mock file system
        target_repo_abs_path = os.path.abspath(self.test_dir)
        source_of_truth_dir = os.path.join(target_repo_abs_path, "project_rules_template")
        mock_exists.return_value = True  # Source of truth exists

        # Mock command line arguments
        args = argparse.Namespace(
            target_repo_path=self.test_dir,
            source_of_truth_dir_name="project_rules_template"
        )

        # Call the handle_sync function
        manage_rules.handle_sync(args)

        # Assert that remove functions were called with correct paths
        mock_rmtree.assert_any_call(os.path.join(target_repo_abs_path, ".cursor"))
        mock_rmtree.assert_any_call(os.path.join(target_repo_abs_path, ".clinerules"))
        mock_rmtree.assert_any_call(os.path.join(target_repo_abs_path, ".roo"))
        mock_remove.assert_called_once_with(os.path.join(target_repo_abs_path, ".windsurfrules"))

        # Assert that rule generation functions were called with correct paths
        self.assertEqual(mock_number_files.call_args_list[0], unittest.mock.call(source_of_truth_dir, os.path.join(target_repo_abs_path, ".cursor"), extension_mode='add_mdc'))
        self.assertEqual(mock_number_files.call_args_list[1], unittest.mock.call(source_of_truth_dir, os.path.join(target_repo_abs_path, ".clinerules"), extension_mode='remove'))
        mock_roocode.assert_called_once_with(source_of_truth_dir, os.path.join(target_repo_abs_path, ".roo"))
        mock_concatenate.assert_called_once_with(source_of_truth_dir, os.path.join(target_repo_abs_path, ".windsurfrules"))

        # Test case where source of truth directory does not exist
        mock_exists.return_value = False
        manage_rules.handle_sync(args)
        mock_number_files.assert_not_called() # Ensure rule generation is skipped
        mock_roocode.assert_not_called()
        mock_concatenate.assert_not_called()

    @patch("src.manage_rules.shutil.rmtree")
    @patch("src.manage_rules.os.remove")
    def test_handle_clean(self, mock_rmtree, mock_remove):
        # Mock command line arguments
        args = argparse.Namespace(
            target_repo_path=self.test_dir,
            source_of_truth_dir_name="project_rules_template"
        )
        target_repo_abs_path = os.path.abspath(self.test_dir)
        source_of_truth_dir = os.path.join(target_repo_abs_path, "project_rules_template")

        # Call the handle_clean function
        manage_rules.handle_clean(args)

        # Assert that remove functions were called with correct paths
        mock_rmtree.assert_any_call(os.path.join(target_repo_abs_path, ".cursor"))
        mock_rmtree.assert_any_call(os.path.join(target_repo_abs_path, ".clinerules"))
        mock_rmtree.assert_any_call(os.path.join(target_repo_abs_path, ".roo"))
        mock_remove.assert_called_once_with(os.path.join(target_repo_abs_path, ".windsurfrules"))
        mock_rmtree.assert_called_with(os.path.abspath(source_of_truth_dir))


if __name__ == '__main__':
    unittest.main()
