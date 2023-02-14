{ buildPythonPackage
, cadquery
}:

buildPythonPackage {

  name = "cq-wild";

  src = ./.;
  format = "pyproject";

  propagatedBuildInputs = [
    cadquery
  ];

}
