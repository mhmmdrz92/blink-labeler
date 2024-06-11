# Blink_Labeler - EEG Artifact Labeler

Blink_Labeler is a desktop application designed to facilitate the labeling of artifacts within EEG data. This tool is particularly useful for researchers and clinicians working in the field of neuroscience.

## Features

- User-friendly Interface: A simple graphical user interface (GUI) built with PyQt5 for easy navigation and data labeling.
- Data Loading: Ability to load EEG data stored in CSV files.
- Artifact Visualization: Plot EEG signals with adjustable parameters for effective visual inspection.
- Labeling: Mark segments of EEG data as containing ocular artifacts (OA) or not (NOA).
- Filtering and Resampling: Preprocess EEG data with built-in filtering and resampling capabilities.
- Result Saving: Export artifact labels to text files for further analysis.

## Requirements

- Python 3.x
- PyQt5
- NumPy
- SciPy
- Matplotlib
- Win32 API (for Windows)

## Installation

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`
3. Run `Blink_UI.py` to launch the application.

## Usage

1. Browse: Select a CSV file containing EEG data.
2. Set Sampling Rate: Adjust the sampling rate if needed.
3. Start Labeling: Click the "Start" button to begin labeling artifacts.
4. Label Segments: Use the "OA" and "NOA" buttons to mark segments.
5. Correction: Go back to previous segments if you need to revise labels.

## Project Structure

- `Blink_UI.py`: Main application script.
- `main_win.py`: Defines the main window and functionality of the UI.
- `plot.py`: Contains functions for plotting EEG data.
- `ui/main.ui`: UI design file.
- `ui/logo.png`: Logo file.
- `results/`: Directory for saving labeled data.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
