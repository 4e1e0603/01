@echo off

if "%1"=="" (
    @echo "no command provided"
    goto :end
)
if "%1"=="build" (
    gfortran -fopenmp source/random_walk.f90 source/random_walk_main.f90 -o build/random_walk_main.exe
    gfortran -fopenmp source/random_walk.f90 source/random_walk_test.f90 -o build/random_walk_test.exe
    goto :end
)
if "%1"=="update" (
    echo commit and push to github
    git add -A
    git commit -am "Update solution"
    git push -u origin main
    goto :end

if "%1"=="updatef" (
    echo commit and force push to github
    git add -A
    git commit --amend -am "Update solution"
    git push -f -u origin main
    goto :end
)
:end