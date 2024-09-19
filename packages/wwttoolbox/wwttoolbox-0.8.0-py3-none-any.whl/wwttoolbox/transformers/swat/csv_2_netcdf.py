from wwttoolbox.transformers.swat.csv_reader import CsvReader
from wwttoolbox.nc import NCTool


class Csv2Netcdf:

    def __init__(self, csv_path: str, netcdf_path: str, name_prefix: str):
        """Instantiates a Csv2Netcdf object.

        Parameters:
        - csv_path (str): The path to the CSV file.
        - netcdf_path (str): The path to the NetCDF file.
        - name_prefix (str): The prefix on the gis ids e.g. 'aqu'
        """
        self.netcdf_path: str = netcdf_path
        self.csv_reader = CsvReader(csv_path=csv_path, name_prefix=name_prefix)
        self.parameters: list[str] = []

    def transform(self):
        """Transforms the CSV file to a NetCDF file."""
        self.load_csv()
        self.set_parameters_to_write()
        self.create_netcdf()
        self.write_parameters()

    def load_csv(self):
        """Loads the CSV file into memory."""
        self.csv_reader.read_csv()

    def set_parameters_to_write(self):
        """Sets the parameters to write to the NetCDF file."""

        col_names = self.csv_reader.get_col_names()

        for col_name in col_names:
            if col_name in [
                "jday",
                "mon",
                "day",
                "yr",
                "unit",
                "gis_id",
                "name",
                "null",
            ]:
                continue
            self.parameters.append(col_name)

    def create_netcdf(self):
        """Creates the NetCDF file."""

        time_data = self.csv_reader.get_time_dimension()
        gis_unit_data = self.csv_reader.get_gis_unit_dimension()

        with NCTool(self.netcdf_path, "w") as tool:
            tool.add_time_dimension()
            tool.add_dimension("gis_unit", len(gis_unit_data))

            tool.add_time_variable()
            tool.add_variable("gis_unit", "long", ["gis_unit"])

            tool.write_time_data(time_data)
            tool.write_data("gis_unit", gis_unit_data)

    def write_parameters(self):
        """Writes the parameters to the NetCDF file."""

        for parameter in self.parameters:
            data = self.csv_reader.get_parameter(parameter, "float")
            unit = self.csv_reader.get_units()[parameter]

            with NCTool(self.netcdf_path, "a") as tool:
                tool.add_variable(parameter, "float", ["time", "gis_unit"])
                tool.add_variable_attribute(parameter, "units", unit)
                tool.write_data(parameter, data)
