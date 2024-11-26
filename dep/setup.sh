pip cache purge
pip install --user -r C:/repos/phecdm/dep/requirements.txt


# # Define the directory you want to add to the PATH
# $directoryToAdd = "C:\Users\xsm7f\AppData\Roaming\Python\Python313"

# # Get the current PATH environment variable
# $currentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)

# # Check if the directory is already in the PATH
# if ($currentPath -notlike "*$directoryToAdd*") {
#     # Add the directory to the PATH
#     $newPath = $currentPath + ";$directoryToAdd"
#     [Environment]::SetEnvironmentVariable("Path", $newPath, [EnvironmentVariableTarget]::Machine)
#     Write-Host "Added $directoryToAdd to PATH."
# } else {
#     Write-Host "$directoryToAdd is already in PATH."
# }
