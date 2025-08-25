from pathlib import Path
import csv
import json


class output:
    @staticmethod
    def output_results(results, result_name = None):
        if result_name:
            path = Path(result_name)

            try:
                if path.suffix == '.txt':
                    with open(path, 'a' if path.exists() else 'w') as f:
                        for key, value in results.items():
                            f.write(f"{key}: {value}\n")

                elif path.suffix == '.csv':
                    mode = 'a' if path.exists() else 'w'
                    with open(path, mode, newline='') as f:
                        writer = csv.writer(f)
                        if mode == 'w':
                            writer.writerow(['URL', 'Status'])
                        for key, value in results.items():
                            writer.writerow([key, value])
                
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









#class Output:
#    @staticmethod
#    def output_results(results, result_name = None):
#        if result_name.endswith(('.txt', 'csv', 'json')) and result_name.exists(): 
#            with open("result_name", "a") as f:
#                f.write(f"{key}: {value}\n")
#                print(f"Results appended to {result_name}")
#                if result_name.endswith(('.txt', 'csv', 'json')) and result_name is not True():
#                    with open("result_name", "x") as f:
#                        for key, value in results.items():
#                            f.write(f"{key}: {value}\n")
#                        print(f"File created and appened to: {result_name}")
#        else:
#            print("No valid file name or path provided, printing results to console:")
#            for key, value in results.items():
#                print(f"{key}: {value}")
#    
#    def file_type(results, result_name, f):
#        if result_name.endswith('.txt'):
#            return 'txt'
#        elif result_name.endswith('.csv'):
#            writer = csv.writer(results)
#            writer.writerows(results, f)
#        elif result_name.endswith('.json'):
#            json.dump(results, f, indent=4)
#        else:
#            raise ValueError("Unsupported file format. Use .txt, .json, or .csv")