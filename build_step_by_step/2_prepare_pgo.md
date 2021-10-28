# Download pgo profile automatically
- From a cmd.exe shell, run the command gclient (without arguments). On first run, gclient will install all the Windows-specific bits needed to work with the code, including msysgit and python.
    ```cmd
    set PATH=path\to\depot_tools;%PATH%
    python3 build/src/tools/update_pgo_profiles.py --target=win64 update --gs-url-base=chromium-optimization-profiles/pgo_profiles
    ```
- Download pgo profile manually<br>
`chrome-win64-*.profdata` in `build\src\chrome\build\pgo_profiles`

- Other files needed, build and copy them to `build\src\third_party\llvm-build\Release+Asserts\bin`
    - llvm-pdbutil.exe
    - llvm-tblgen.exe
    - llvm-undname.exe
