def run(self, root="."):
    files = self.scanner.scan(root)

    results = []
    dependencies = {}

    for file in files:
        results.append(
            self.validator.validate(file)
        )

        dependencies[str(file)] = (
            self.dependency.analyze(file)
        )

    report = self.health.generate(
        files,
        results
    )

    advice = self.advisor.advise(report)

    return {
        "report": report,
        "advice": advice,
        "dependencies": dependencies
    }
