import os
import re

directories = ["DP", "DP-2", "DP-3"]
base_dir = r"z:\Stuff\Temp projects\DSA"

for directory in directories:
    dir_path = os.path.join(base_dir, directory)
    if not os.path.isdir(dir_path):
        continue
    print(f"=== Directory: {directory} ===")
    for filename in sorted(os.listdir(dir_path)):
        if not filename.endswith(".md") or filename in ["PROGRESS.md", "progressv2.md"]:
            continue
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"  File: {filename}")
        # Find all problem headers (### [Number]. [Name] or similar)
        # Problems start with ### followed by digit or specific format
        problems = re.split(r'\n###\s+', content)
        if len(problems) <= 1:
            continue
        
        # The first part is the introduction/header
        for prob in problems[1:]:
            lines = prob.strip().split('\n')
            title = lines[0]
            
            # Check for sub-headings
            has_memo = any(re.search(r'####.*(memo|top-down)', line, re.IGNORECASE) for line in lines)
            has_tab = any(re.search(r'####.*(tab|bottom-up)', line, re.IGNORECASE) for line in lines)
            has_space_opt = any(re.search(r'####.*(space|opt)', line, re.IGNORECASE) for line in lines)
            
            print(f"    - Title: {title}")
            print(f"      Memoization: {'Yes' if has_memo else 'No'}")
            print(f"      Tabulation:  {'Yes' if has_tab else 'No'}")
            print(f"      Space Opt:   {'Yes' if has_space_opt else 'No'}")
