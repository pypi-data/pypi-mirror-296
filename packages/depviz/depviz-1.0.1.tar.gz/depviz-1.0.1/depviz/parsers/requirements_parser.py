def parse_requirements(file_path):
    dependencies = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # Extract the package name without version specifiers
                package = (
                    line.split("[")[0]
                    .split("==")[0]
                    .split(">=")[0]
                    .split("<=")[0]
                    .strip()
                )
                dependencies.append(package)
    return dependencies
