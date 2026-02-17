# [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?logo=buy-me-a-coffee)](https://buymeacoffee.com/succinctrecords)

# Audio to FLAC Converter

A powerful, interactive command-line tool that intelligently converts any audio format to FLAC (Free Lossless Audio Codec) with automatic quality detection and preservation of metadata and artwork.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

## Features

- 🎵 **Universal Format Support** - Converts from M4A, MP3, WAV, AAC, OGG, Opus, WMA, APE, AIFF, and more
- 🔍 **Intelligent Codec Detection** - Automatically identifies lossless vs lossy source files
- ⚠️ **Quality Warnings** - Alerts you when converting lossy files (which won't improve quality)
- 🎨 **Metadata Preservation** - Keeps artist, album, title, and all other tags
- 🖼️ **Artwork Preservation** - Maintains embedded album covers
- ⚙️ **Configurable Compression** - Choose FLAC compression levels 0-8
- 🗑️ **Optional Cleanup** - Delete original files after successful conversion
- 📁 **Flexible Output** - Convert in-place or to a separate subdirectory
- 🔐 **Permission Management** - Automatically set file permissions
- 🎨 **Beautiful Interface** - Color-coded, easy-to-read terminal output
- 📊 **Detailed Statistics** - See file sizes, compression ratios, and conversion status

## Screenshots

```
============================================================
                  Audio to FLAC Converter
============================================================

Scanning Current Directory
ℹ Directory: /home/user/Music/Album
✓ Found 12 audio file(s)

Analyzing files...

ℹ Analyzing: 01 - Track Name.m4a
  Codec: ALAC (LOSSLESS)
  Sample Rate: 44100 Hz, Bit Depth: 16, Channels: 2
  Has embedded artwork

✓ Successfully converted: 12/12
```

## Requirements

- **Operating System:** Linux (Debian/Ubuntu recommended)
- **Python:** 3.6 or higher
- **ffmpeg:** For audio conversion and analysis
- **Root/sudo access:** For installation to `/usr/local/bin/`

## Installation

### Quick Install (Recommended)

```bash
# Download the script
curl -O https://raw.githubusercontent.com/WB2024/Convert-Audio-to-FLAC/main/audio-to-flac.py

# Make it executable
chmod +x audio-to-flac.py

# Move to system bin directory
sudo mv audio-to-flac.py /usr/local/bin/

# Create convenient alias (optional)
sudo ln -s /usr/local/bin/audio-to-flac.py /usr/local/bin/audio-to-flac
```

### Manual Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/WB2024/Convert-Audio-to-FLAC.git
   cd Convert-Audio-to-FLAC
   ```

2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg python3
   ```

3. **Install the script:**
   ```bash
   chmod +x audio-to-flac.py
   sudo cp audio-to-flac.py /usr/local/bin/
   sudo ln -s /usr/local/bin/audio-to-flac.py /usr/local/bin/audio-to-flac
   ```

4. **Verify installation:**
   ```bash
   audio-to-flac.py --help
   ```

## Usage

### Basic Usage

Navigate to any directory containing audio files and run:

```bash
audio-to-flac.py
```

Or use the shorter alias:

```bash
audio-to-flac
```

### Workflow

1. **Scan** - The tool scans the current directory for audio files
2. **Analyze** - Each file is analyzed to determine codec type (lossless/lossy)
3. **Summary** - Review what will be converted with quality warnings
4. **Configure** - Choose conversion options interactively:
   - FLAC compression level (0-8)
   - Preserve metadata (yes/no)
   - Preserve artwork (yes/no)
   - Delete originals (yes/no)
   - Create output subdirectory (yes/no)
   - Set file permissions (yes/no)
5. **Convert** - Files are converted with progress tracking
6. **Complete** - View final statistics and results

### Example Session

```bash
# Navigate to your music folder
cd ~/Music/NewAlbum

# Run the converter
audio-to-flac

# Follow the interactive prompts
# ✓ Compression level: 8
# ✓ Preserve metadata: Yes
# ✓ Preserve artwork: Yes
# ✓ Delete originals: No
# ✓ Output subdirectory: Yes
# ✓ Fix permissions: Yes

# Results will be in ~/Music/NewAlbum/FLAC/
```

## Supported Formats

### Input Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| M4A/AAC | `.m4a`, `.aac` | Most common Apple format |
| ALAC | `.m4a` | Apple Lossless (true lossless) |
| MP3 | `.mp3` | Lossy format |
| WAV | `.wav` | Uncompressed lossless |
| FLAC | `.flac` | Already FLAC (skipped) |
| OGG Vorbis | `.ogg` | Lossy format |
| Opus | `.opus` | Modern lossy codec |
| WMA | `.wma` | Windows Media Audio |
| APE | `.ape` | Monkey's Audio (lossless) |
| AIFF | `.aiff` | Apple uncompressed |
| TTA | `.tta` | True Audio (lossless) |
| WavPack | `.wv` | Lossless compression |
| Musepack | `.mpc` | Lossy format |

### Output Format

- **FLAC** (`.flac`) - Free Lossless Audio Codec
  - Compression levels 0-8 (8 = maximum compression)
  - Metadata support (Vorbis comments)
  - Embedded artwork support
  - Wide compatibility

## Understanding Quality

### Lossless → FLAC ✅

When converting from lossless formats (ALAC, WAV, APE, etc.), the conversion is **bit-perfect**:
- No quality loss
- Smaller file size (FLAC compression)
- Metadata preserved
- **Recommended**

### Lossy → FLAC ⚠️

When converting from lossy formats (MP3, AAC, OGG, etc.):
- Creates larger files
- **Does NOT improve quality**
- Original compression artifacts remain
- Only useful for format standardization

The tool will **warn you** when converting lossy files.

## FLAC Compression Levels

| Level | Speed | File Size | Quality |
|-------|-------|-----------|---------|
| 0 | Fastest | Largest | Identical |
| 5 | Medium | Medium | Identical |
| 8 | Slowest | Smallest | Identical |

**Note:** All compression levels are lossless - higher levels just compress better at the cost of encoding time.

**Recommended:** Level 8 for archival, Level 5 for speed.

## Configuration Options

### Interactive Prompts

| Option | Default | Description |
|--------|---------|-------------|
| Compression Level | 8 | FLAC compression (0-8) |
| Preserve Metadata | Yes | Keep artist, album, title, etc. |
| Preserve Artwork | Yes | Keep embedded album covers |
| Delete Originals | No | Remove source files after conversion |
| Output Subdirectory | No | Create `FLAC/` folder for output |
| Fix Permissions | Yes | Set files to 777 permissions |

## Technical Details

### How It Works

1. **Scanning:** Uses Python's `pathlib` to find audio files by extension
2. **Analysis:** Uses `ffprobe` (part of ffmpeg) to extract codec information
3. **Classification:** Compares codec against known lossless/lossy lists
4. **Conversion:** Uses `ffmpeg` with optimized parameters for each file
5. **Validation:** Checks output file exists and reports size comparison

### Codec Detection

The tool maintains lists of known codecs:

**Lossless Codecs:**
- FLAC, ALAC, APE, WavPack, TTA, WAV, PCM variants, AIFF

**Lossy Codecs:**
- AAC, MP3, Opus, Vorbis, WMA, AC3, DTS, Musepack

If a codec is not in either list, it's marked as "unknown" and you're asked to proceed.

### FFmpeg Command Structure

```bash
ffmpeg -y -i "input.m4a" \
  -map 0:a:0 \                    # Map first audio stream
  -c:a flac \                     # Use FLAC codec
  -compression_level 8 \          # Maximum compression
  -map 0:v:0? \                   # Map video (artwork) if exists
  -c:v copy \                     # Copy artwork without re-encoding
  -map_metadata 0 \               # Preserve all metadata
  "output.flac"
```

## Troubleshooting

### "ffmpeg is not installed"

**Solution:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### "Permission denied"

**Solution:**
```bash
sudo chmod +x /usr/local/bin/audio-to-flac.py
```

Or run from any directory:
```bash
python3 /usr/local/bin/audio-to-flac.py
```

### "No audio files found"

**Causes:**
- No supported audio files in current directory
- Files have unusual extensions

**Solution:**
```bash
# Check what files exist
ls -lh

# Make sure you're in the right directory
pwd
```

### Conversion fails for specific file

**Check the file:**
```bash
ffprobe "problem_file.m4a"
```

The file might be corrupted or use an unsupported codec variant.

### Output files owned by root

This happens when running with `sudo`. The script includes permission fixing, but you can manually fix:

```bash
sudo chown -R $USER:$USER /path/to/output
sudo chmod -R 755 /path/to/output
```

## FAQ

**Q: Will converting MP3 to FLAC improve quality?**  
A: No. You cannot recover quality lost during lossy compression. The tool will warn you about this.

**Q: Should I delete my original ALAC files after converting to FLAC?**  
A: Both are lossless, so it's safe if you want to save space or prefer FLAC's broader compatibility.

**Q: What's the best compression level?**  
A: Level 8 for archival storage, level 5 for faster encoding. Both are lossless.

**Q: Can I convert an entire music library?**  
A: Yes, but process one album folder at a time. The script operates on the current directory only.

**Q: Does this work on macOS or Windows?**  
A: It's designed for Linux but could work on macOS with minor modifications. Windows would require WSL or significant changes.

**Q: Will this preserve gapless playback?**  
A: Yes, FLAC supports gapless playback and metadata is preserved.

## Use Cases

### Convert Apple Music Downloads (ALAC → FLAC)

```bash
cd ~/Music/AppleMusic/Album
audio-to-flac
# Choose: Yes to subdirectory, Yes to delete originals
```

### Standardize Mixed Library

```bash
cd ~/Music/MixedFormats
audio-to-flac
# Converts everything to FLAC for consistency
```

### Archive WAV Files

```bash
cd ~/Audio/WAVFiles
audio-to-flac
# Reduces file size by 40-60% without quality loss
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Development Setup

```bash
git clone https://github.com/WB2024/Convert-Audio-to-FLAC.git
cd Convert-Audio-to-FLAC
# Make changes to audio-to-flac.py
# Test your changes
python3 audio-to-flac.py
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Author

**WB2024**
- GitHub: [@WB2024](https://github.com/WB2024)

## Acknowledgments

- [FFmpeg](https://ffmpeg.org/) - The backbone of audio conversion
- [FLAC](https://xiph.org/flac/) - Free Lossless Audio Codec
- Python community for excellent libraries and tools

## Changelog

### v1.0.0 (2025-02-17)
- Initial release
- Support for 15+ audio formats
- Intelligent codec detection
- Interactive configuration
- Metadata and artwork preservation
- Comprehensive error handling

## See Also

- **[CD Ripper](https://github.com/WB2024/CD-Ripper)** - Companion tool for ripping CDs to FLAC
- **[FFmpeg Documentation](https://ffmpeg.org/documentation.html)**
- **[FLAC Format Specification](https://xiph.org/flac/format.html)**

---

**Happy Converting! 🎵**
