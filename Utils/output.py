from pathlib import Path
import csv
import json

#main class for output
class output:
    @staticmethod
    def output_results(results, result_name = None):
        if result_name:
            path = Path(result_name)

            #Logic to save results as a text file
            try:
                if path.suffix == '.txt':
                    with open(path, 'a' if path.exists() else 'w') as f:
                        for key, value in results.items():
                            if isinstance(value, dict):
                                f.write(f"{key}:\n")
                                for k, v in value.items():
                                    f.write(f"  {k}: {v}\n")
                                f.write("\n")
                            else:
                                f.write(f"{key}: {value}\n")
                        
            #Logic to save results as a csv file
                elif path.suffix == '.csv':
                    mode = 'a' if path.exists() else 'w'
                    with open(path, mode, newline='') as f:
                        writer = csv.writer(f)
                        if mode == 'w':
                            writer.writerow(['URL', 'Status'])
                        for key, value in results.items():
                            writer.writerow([key, value])
                
            #Logic to save results as a json file
                elif path.suffix == '.json':
                    if path.exists():
                        with open(path, 'r') as f:
                            existing_data = json.load(f)
                            existing_data.update(results)
                            results = existing_data
                    
                    with open(path, 'w') as f:
                        json.dump(results, f, indent=4)

                else:
                    print("Unsupported file format. Please use .txt, .csv, or .json")
                
                print(f"Results saved to {result_name} saved at location {path}")
                
            except Exception as e:
                print(f"Error saving results: {e}")
                print("Printing results to console instead:")
                for key, value in results.items():
                    print(f"{key}: {value}")
        
        else:
            print("\nResults:")
            print("=" * 50)
            for key, value in results.items():
                print(f"{key}: {value}")

        return results

