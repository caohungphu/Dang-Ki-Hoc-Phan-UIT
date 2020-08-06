from cx_Freeze import setup, Executable

setup(name = "DangKiHocPhanUIT" ,
      version = "2.0" ,
      description = "DangKiHocPhanUIT" ,
      executables = [Executable("dkhp.py")])