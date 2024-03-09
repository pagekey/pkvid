from pkvid.driver import BlenderDriver


if __name__ == "__main__":
    driver = BlenderDriver(debug=True)
    driver.save_project('hi.blend')
    driver.execute()
