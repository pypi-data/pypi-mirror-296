import os
import unittest
from unittest.mock import MagicMock, patch

from kubernetes.client.models import V1EnvVar
from ..cogflow import (
    plugin_config,
    pipeline,
    create_component_from_func,
    client,
    input_path,
    output_path,
    serve_model_v2,
    serve_model_v1,
    get_model_url,
    load_component,
    delete_pipeline,
)
from ..cogflow.plugins.kubeflowplugin import KubeflowPlugin, CogContainer


class TestKubeflowPlugin(unittest.TestCase):
    def setUp(self):
        self.kfp_plugin = KubeflowPlugin()

    @patch("kfp.dsl.pipeline")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_pipeline_with_name_and_description(
        self, mock_plugin_activation, mock_pipeline
    ):
        pipeline()
        mock_pipeline.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("kfp.components.create_component_from_func")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_create_component_from_func(
        self, mock_plugin_activation, mock_create_component
    ):
        func = MagicMock()
        create_component_from_func(func)
        mock_create_component.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("kfp.Client")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_client(self, mock_plugin_activation, mock_client):
        # Arrange
        client()

        # Assertion
        mock_client.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("kfp.components.load_component_from_url")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_load_component_from_url_success(
        self, mock_plugin_activation, mock_load_component
    ):
        # Mock a successful component loading
        expected_component_spec = MagicMock()
        mock_load_component.return_value = expected_component_spec

        # Define a sample URL
        url = "http://example.com/component.tar.gz"

        # Call the function under test
        result = load_component(url=url)

        # Assert that the function returns the expected component specification
        self.assertEqual(result, expected_component_spec)

        # Assert that load_component_from_url was called with the correct URL
        mock_load_component.assert_called_once_with(url)
        mock_plugin_activation.assert_called_once()

    @patch("kfp.components.InputPath")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_input_path(self, mock_plugin_activation, mock_input):
        # Define a sample label for the input path
        label = "input_data"

        input_path_val = input_path(label)
        mock_input.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("kfp.components.OutputPath")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_output_path(self, mock_plugin_activation, mock_output):
        # Define a sample label for the input path
        label = "output_data"

        input_path = output_path(label)
        mock_output.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch.dict(
        os.environ,
        {
            "TRACKING_URI": "tracking_uri_value",
            "S3_ENDPOINT_URL": "s3_endpoint_url_value",
            "ACCESS_KEY_ID": "access_key_id_value",
            "SECRET_ACCESS_KEY": "secret_access_key_value",
            "ADDITIONAL_VAR_1": "additional_value_1",
            "ADDITIONAL_VAR_2": "additional_value_2",
        },
    )
    def test_add_model_access(self):
        # Create an instance of CogContainer
        container = CogContainer()

        # Mock plugin_config to use the environment variable names directly
        with patch.object(plugin_config, "TRACKING_URI", "TRACKING_URI"), patch.object(
            plugin_config, "S3_ENDPOINT_URL", "S3_ENDPOINT_URL"
        ), patch.object(plugin_config, "ACCESS_KEY_ID", "ACCESS_KEY_ID"), patch.object(
            plugin_config, "SECRET_ACCESS_KEY", "SECRET_ACCESS_KEY"
        ):
            # Call the add_model_access method
            container_with_env_vars = container.add_model_access()

            # Assert that the returned value is an instance of CogContainer
            self.assertIsInstance(container_with_env_vars, CogContainer)

            # Expected environment variables explicitly listed in the method
            expected_env_vars = [
                V1EnvVar(name="TRACKING_URI", value="tracking_uri_value"),
                V1EnvVar(name="S3_ENDPOINT_URL", value="s3_endpoint_url_value"),
                V1EnvVar(name="ACCESS_KEY_ID", value="access_key_id_value"),
                V1EnvVar(name="SECRET_ACCESS_KEY", value="secret_access_key_value"),
            ]

            # Expected additional environment variables from os.environ
            additional_env_vars = [
                V1EnvVar(name="ADDITIONAL_VAR_1", value="additional_value_1"),
                V1EnvVar(name="ADDITIONAL_VAR_2", value="additional_value_2"),
            ]

            all_expected_env_vars = expected_env_vars + additional_env_vars

            # Assert that all expected environment variables are added correctly
            for expected_env_var in all_expected_env_vars:
                self.assertIn(expected_env_var, container_with_env_vars.env)

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_serve_model_v2(self, mock_plugin_activation):
        # Patch Kubernetes client to avoid loading kube config
        with patch("kubernetes.config.load_kube_config"):
            model_uri = "sample_model_uri"
            name = "test_model_name"

            # Call the function and assert that it raises MaxRetryError
            with self.assertRaises(Exception):
                serve_model_v2(model_uri, name)
            mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_serve_model_v2_no_name(self, mock_plugin_activation):
        with patch("kubernetes.config.load_kube_config"):
            model_uri = "sample_model_uri"

            # Call the function and assert that it raises MaxRetryError
            with self.assertRaises(Exception):
                self.kfp_plugin.serve_model_v2(model_uri)
            mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_serve_model_v1_with_exception(self, mock_plugin_activation):
        # Define input parameters
        model_uri = "example_model_uri"
        name = "test_model_name"

        # Call the function and assert that it raises MaxRetryError
        with self.assertRaises(Exception):
            serve_model_v1(model_uri, name)
        mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_get_model_url(self, mock_plugin_activation):
        model_name = "test_model"

        with self.assertRaises(Exception):
            # Call the method you're testing here
            get_model_url(model_name)
        mock_plugin_activation.assert_called_once()

    @patch("requests.delete")
    @patch("requests.get")
    @patch("os.getenv")
    @patch("cogflow.cogflow.plugins.kubeflowplugin.KubeflowPlugin.client")
    def test_delete_pipeline(
        self, mock_client, mock_env, mock_request_get, mock_request_delete
    ):
        # Arrange
        mock_env.side_effect = lambda x: {
            "API_BASEPATH": "http://randomn",
            "COGFLOW_CONFIG_FILE_PATH": "/path",
        }[x]
        mock_request_get.return_value.status_code = 200
        mock_request_delete.return_value.status_code = 200
        plugin = KubeflowPlugin()
        mock_client_instance = mock_client.return_value
        pipeline_id = "test_pipeline_id"

        # Act
        delete_pipeline(pipeline_id)

        # Assert
        mock_client_instance.delete_pipeline.assert_called_once_with(
            pipeline_id=pipeline_id
        )

    @patch("cogflow.cogflow.plugins.kubeflowplugin.KubeflowPlugin.client")
    def test_list_pipeline_versions(self, mock_client):
        # Arrange
        plugin = KubeflowPlugin()
        mock_client_instance = mock_client.return_value
        pipeline_id = "test_pipeline_id"
        expected_response = "expected_response"
        mock_client_instance.list_pipeline_versions.return_value = expected_response

        # Act
        response = plugin.list_pipeline_versions(pipeline_id)

        # Assert
        mock_client_instance.list_pipeline_versions.assert_called_once_with(
            pipeline_id=pipeline_id
        )
        self.assertEqual(response, expected_response)

    @patch("cogflow.cogflow.plugins.kubeflowplugin.KubeflowPlugin.client")
    def test_delete_pipeline_version(self, mock_client):
        # Arrange
        plugin = KubeflowPlugin()
        mock_client_instance = mock_client.return_value
        version_id = "test_version_id"

        # Act
        plugin.delete_pipeline_version(version_id)

        # Assert
        mock_client_instance.delete_pipeline_version.assert_called_once_with(
            version_id=version_id
        )

    @patch("cogflow.cogflow.plugins.kubeflowplugin.KubeflowPlugin.client")
    def test_delete_runs(self, mock_client):
        # Arrange
        plugin = KubeflowPlugin()
        mock_client_instance = mock_client.return_value
        mock_client_instance.runs = MagicMock()
        run_ids = [1, 2]

        # Act
        plugin.delete_runs(run_ids)

        # Assert
        calls = [unittest.mock.call(id=1), unittest.mock.call(id=2)]
        mock_client_instance.runs.delete_run.assert_has_calls(calls, any_order=True)
        self.assertEqual(mock_client_instance.runs.delete_run.call_count, 2)


if __name__ == "__main__":
    unittest.main()
