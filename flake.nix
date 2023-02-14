{

  inputs.cq-flake.url = github:thelegy/cq-flake;
  inputs.nixpkgs = {
    url = github:NixOS/nixpkgs;
    follows = "cq-flake/nixpkgs";
  };

  outputs = { nixpkgs, cq-flake, self }: {

    overlays.default = final: prev: {
      pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
        (pfinal: pprev: {
          cq-wild = pfinal.callPackage ./default.nix {};
        })
      ];
    };

    packages.x86_64-linux = let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        overlays = [
          cq-flake.overlays.default
          self.overlays.default
        ];
      };
    in {
      default = pkgs.pythonCQ.withPackages (p: [p.cq-wild]);
    };

    devShells.x86_64-linux = let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        overlays = [
          cq-flake.overlays.default
          self.overlays.default
        ];
      };
    in {
      default = pkgs.mkShell {
        inputsFrom = [ pkgs.pythonCQPackages.cq-wild ];
        nativeBuildInputs = [ pkgs.cq-editor ];
      };
    };

  };

}
