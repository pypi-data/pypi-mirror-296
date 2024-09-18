import json
import os

class DbtProcessor:
    def __init__(self, manifest_path, run_results_path):
        self.manifest_path = manifest_path
        self.run_results_path = run_results_path
        self.manifest_data = self._load_json(manifest_path)
        self.run_results_data = self._load_json(run_results_path)

    def _load_json(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, 'r') as file:
            return json.load(file)

    def process(self):
        summary = {
            "nodes": self._process_nodes(),
            "run_results": self._process_run_results()
        }
        return summary

    def _process_nodes(self):
        nodes = self.manifest_data.get('nodes', {})
        processed_nodes = []
        for node_id, node in nodes.items():
            processed_nodes.append({
                "unique_id": node.get("unique_id"),
                "name": node.get("name"),
                "resource_type": node.get("resource_type"),
                "depends_on": node.get("depends_on", {}).get("nodes", []),
                "columns": node.get("columns", {}),
                "description": node.get("description"),
                "tags": node.get("tags", []),
                "meta": node.get("meta", {}),
                "database": node.get("database"),
                "schema": node.get("schema"),
                "alias": node.get("alias"),
                "compiled_code": node.get("compiled_code"),
            })
        return processed_nodes

    def _process_run_results(self):
        run_results = self.run_results_data.get('results', [])
        processed_results = []
        for result in run_results:
            processed_results.append({
                "unique_id": result.get("unique_id"),
                "status": result.get("status"),
                "execution_time": result.get("execution_time"),
                "message": result.get("message"),
                "adapter_response": result.get("adapter_response"),
                "timing": result.get("timing"),
                "thread_id": result.get("thread_id"),
                "execution_time": result.get("execution_time"),
                "failures": result.get("failures")
            })
        return processed_results

    def print_summary(self):
        summary = self.process()
        print(json.dumps(summary, indent=4))


# def main():
#     manifest_path = '/Users/ankur.kumar/Documents/do_extra/DBT/do_dbt_test/target/manifest.json'
#     run_results_path = '/Users/ankur.kumar/Documents/do_extra/DBT/do_dbt_test/target/run_results.json'

#     processor = DbtProcessor(manifest_path, run_results_path)
#     processor.print_summary()

# if __name__ == "__main__":
#     main()
