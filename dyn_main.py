import tracemalloc
import main

# python dyn_main.py


def run():
    tracemalloc.start()
    main.main()

    current, peak = tracemalloc.get_traced_memory()
    current_kb = current / 1024
    peak_kb = peak / 1024
    print(
        f"\n[tracemalloc] Current: {current_kb:.1f} KB; Peak: {peak_kb:.1f} KB"
    )

    tracemalloc.stop()


if __name__ == "__main__":
    run()
