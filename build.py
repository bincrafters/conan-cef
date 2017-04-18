from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="inexorgame", channel="stable")
    builder.add_common_builds(pure_c=False,visual_versions=["10", "12", "14", "15"])
    builder.run()
