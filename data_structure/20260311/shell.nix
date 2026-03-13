{ pkgs ? import <nixpkgs> {} }:

let
  # 定义 Python 及其所需的库
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    networkx
    matplotlib
    # 如果你在 Linux 上遇到图形界面显示问题，可以取消下面 tkinter 的注释
    # tkinter 
  ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
  ];

  shellHook = ''
    echo "环境已就绪！"
    echo "已激活: networkx, matplotlib"
  '';
}