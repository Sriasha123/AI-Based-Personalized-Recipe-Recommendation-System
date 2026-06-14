def clean_steps(steps):
    """
    Convert Food.com step format into clean list of steps
    """
    if not steps:
        return []

    # Food.com format: c("step1","step2")
    if isinstance(steps, str) and steps.startswith("c("):
        steps = steps[2:-1]  # remove c( and )
        return [
            s.strip().strip('"')
            for s in steps.split('",')
        ]

    # Already clean
    if isinstance(steps, list):
        return steps

    return [str(steps)]
