@echo off
REM Uganda Tech Connect - TypeScript Build Script for Windows
REM This script compiles TypeScript files and sets up the development environment

echo 🚀 Building Uganda Tech Connect TypeScript modules...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    echo    Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo ✅ Node.js and npm are available

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo 📦 Installing TypeScript dependencies...
    npm install
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    
    echo ✅ Dependencies installed successfully
) else (
    echo ✅ Dependencies already installed
)

REM Clean previous build
if exist "dist" (
    echo 🧹 Cleaning previous build...
    rmdir /s /q dist
)

REM Compile TypeScript
echo 🔨 Compiling TypeScript files...
npx tsc

if %errorlevel% equ 0 (
    echo ✅ TypeScript compilation successful!
    
    echo 📁 Generated files:
    if exist "dist" (
        for /r dist %%f in (*.js) do (
            echo    - %%f
        )
    )
    
    echo.
    echo 🎉 Build completed successfully!
    echo.
    echo 📋 Next steps:
    echo    1. Start your Django development server
    echo    2. Open the test file: test_tailwind.html
    echo    3. Check browser console for TypeScript integration status
    echo.
    echo 💡 For development with auto-compilation, run:
    echo    npm run dev
    
) else (
    echo ❌ TypeScript compilation failed
    echo    Please check the errors above and fix them
    pause
    exit /b 1
)

echo.
echo Press any key to continue...
pause >nul
