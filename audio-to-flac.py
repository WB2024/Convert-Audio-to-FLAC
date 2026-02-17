#!/usr/bin/env python3
"""
Audio to FLAC Converter
Intelligently converts any audio format to FLAC with quality preservation
"""

import os
import subprocess
import sys
import json
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AudioConverter:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.audio_extensions = [
            '.m4a', '.mp3', '.wav', '.aac', '.ogg', '.opus', 
            '.wma', '.ape', '.alac', '.aiff', '.flac', '.mka',
            '.mp2', '.ac3', '.dts', '.tta', '.wv', '.mpc'
        ]
        
        # Lossless codecs
        self.lossless_codecs = [
            'flac', 'alac', 'ape', 'wavpack', 'tta', 'wav', 
            'pcm_s16le', 'pcm_s24le', 'pcm_s32le', 'pcm_f32le',
            'aiff', 'truehd', 'mlp'
        ]
        
        # Lossy codecs
        self.lossy_codecs = [
            'aac', 'mp3', 'opus', 'vorbis', 'wmav1', 'wmav2',
            'ac3', 'eac3', 'dts', 'mp2', 'musepack'
        ]
        
        self.files_to_convert = []
        self.conversion_stats = {
            'lossless': [],
            'lossy': [],
            'already_flac': [],
            'errors': []
        }
        self.output_dir = None
        
    def print_header(self, text):
        """Print a formatted header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    
    def print_success(self, text):
        """Print success message"""
        print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")
    
    def print_error(self, text):
        """Print error message"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")
    
    def print_info(self, text):
        """Print info message"""
        print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")
    
    def print_warning(self, text):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")
    
    def run_command(self, command, capture_output=True):
        """Run a shell command"""
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return result.returncode, result.stdout, result.stderr
            else:
                result = subprocess.run(command, shell=True)
                return result.returncode, None, None
        except Exception as e:
            return 1, None, str(e)
    
    def yes_no_prompt(self, question, default=True):
        """Ask a yes/no question"""
        default_text = "Y/n" if default else "y/N"
        while True:
            response = input(f"{Colors.OKBLUE}{question} ({default_text}): {Colors.ENDC}").lower().strip()
            if response == '':
                return default
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                self.print_warning("Please answer 'y' or 'n'")
    
    def fix_permissions(self, path):
        """Set permissions to 777 for a file or directory"""
        try:
            os.chmod(path, 0o777)
            return True
        except Exception as e:
            self.print_warning(f"Could not set permissions for {path}: {e}")
            return False
    
    def fix_permissions_recursive(self, directory):
        """Set permissions to 777 recursively for directory and all contents"""
        try:
            # Fix the directory itself
            os.chmod(directory, 0o777)
            
            # Fix all files and subdirectories
            for root, dirs, files in os.walk(directory):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o777)
            
            return True
        except Exception as e:
            self.print_warning(f"Could not set permissions recursively: {e}")
            return False
    
    def get_audio_info(self, filepath):
        """Get detailed audio information using ffprobe"""
        cmd = f'ffprobe -v quiet -print_format json -show_format -show_streams "{filepath}"'
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode != 0:
            return None
        
        try:
            data = json.loads(stdout)
            
            # Find audio stream
            audio_stream = None
            video_stream = None
            
            for stream in data.get('streams', []):
                if stream.get('codec_type') == 'audio' and not audio_stream:
                    audio_stream = stream
                elif stream.get('codec_type') == 'video':
                    video_stream = stream
            
            if not audio_stream:
                return None
            
            info = {
                'codec': audio_stream.get('codec_name', 'unknown'),
                'sample_rate': audio_stream.get('sample_rate', 'unknown'),
                'channels': audio_stream.get('channels', 'unknown'),
                'bit_depth': audio_stream.get('bits_per_sample', audio_stream.get('bits_per_raw_sample', 'unknown')),
                'bitrate': audio_stream.get('bit_rate', data.get('format', {}).get('bit_rate', 'unknown')),
                'duration': data.get('format', {}).get('duration', 'unknown'),
                'has_video': video_stream is not None,
                'has_metadata': bool(data.get('format', {}).get('tags', {})),
                'metadata': data.get('format', {}).get('tags', {})
            }
            
            # Determine if lossless or lossy
            codec = info['codec'].lower()
            if codec in self.lossless_codecs or 'pcm' in codec:
                info['type'] = 'lossless'
            elif codec in self.lossy_codecs:
                info['type'] = 'lossy'
            else:
                info['type'] = 'unknown'
            
            return info
            
        except json.JSONDecodeError:
            return None
    
    def scan_directory(self):
        """Scan current directory for audio files"""
        self.print_header("Scanning Current Directory")
        self.print_info(f"Directory: {self.current_dir}")
        
        files_found = []
        
        for ext in self.audio_extensions:
            for filepath in Path(self.current_dir).glob(f"*{ext}"):
                if filepath.is_file():
                    files_found.append(str(filepath))
        
        if not files_found:
            self.print_warning("No audio files found in current directory")
            return False
        
        self.print_success(f"Found {len(files_found)} audio file(s)")
        
        # Analyze each file
        print(f"\n{Colors.BOLD}Analyzing files...{Colors.ENDC}\n")
        
        for filepath in sorted(files_found):
            filename = os.path.basename(filepath)
            self.print_info(f"Analyzing: {filename}")
            
            info = self.get_audio_info(filepath)
            
            if not info:
                self.print_error(f"  Could not analyze file")
                continue
            
            # Display info
            codec = info['codec']
            file_type = info['type']
            sample_rate = info['sample_rate']
            bit_depth = info['bit_depth']
            
            if file_type == 'lossless':
                color = Colors.OKGREEN
                type_text = "LOSSLESS"
            elif file_type == 'lossy':
                color = Colors.WARNING
                type_text = "LOSSY"
            else:
                color = Colors.OKCYAN
                type_text = "UNKNOWN"
            
            print(f"  {color}Codec: {codec.upper()} ({type_text}){Colors.ENDC}")
            print(f"  Sample Rate: {sample_rate} Hz, Bit Depth: {bit_depth}, Channels: {info['channels']}")
            
            if info['has_video']:
                print(f"  {Colors.OKCYAN}Has embedded artwork{Colors.ENDC}")
            
            # Check if already FLAC
            if codec == 'flac':
                self.print_warning(f"  Already FLAC - will skip")
                self.conversion_stats['already_flac'].append(filename)
            else:
                self.files_to_convert.append({
                    'path': filepath,
                    'filename': filename,
                    'info': info
                })
                
                if file_type == 'lossless':
                    self.conversion_stats['lossless'].append(filename)
                elif file_type == 'lossy':
                    self.conversion_stats['lossy'].append(filename)
            
            print()
        
        return len(self.files_to_convert) > 0
    
    def show_summary(self):
        """Show conversion summary and warnings"""
        self.print_header("Conversion Summary")
        
        if self.conversion_stats['lossless']:
            self.print_success(f"Lossless files (true conversion): {len(self.conversion_stats['lossless'])}")
            for f in self.conversion_stats['lossless']:
                print(f"  • {f}")
        
        if self.conversion_stats['lossy']:
            self.print_warning(f"\nLossy files (quality cannot be improved): {len(self.conversion_stats['lossy'])}")
            for f in self.conversion_stats['lossy']:
                print(f"  • {f}")
            
            print(f"\n{Colors.WARNING}{Colors.BOLD}WARNING:{Colors.ENDC}")
            print(f"{Colors.WARNING}Converting lossy → FLAC will create larger files WITHOUT quality improvement.{Colors.ENDC}")
            print(f"{Colors.WARNING}The original quality loss cannot be recovered.{Colors.ENDC}")
        
        if self.conversion_stats['already_flac']:
            self.print_info(f"\nAlready FLAC (will skip): {len(self.conversion_stats['already_flac'])}")
        
        print(f"\n{Colors.BOLD}Total files to convert: {len(self.files_to_convert)}{Colors.ENDC}")
    
    def get_conversion_options(self):
        """Get user preferences for conversion"""
        self.print_header("Conversion Options")
        
        options = {}
        
        # FLAC compression level
        print(f"{Colors.BOLD}FLAC Compression Level:{Colors.ENDC}")
        print("  0 = Fastest, largest files")
        print("  5 = Default, balanced")
        print("  8 = Slowest, smallest files (recommended)")
        
        while True:
            try:
                level = input(f"{Colors.OKBLUE}Choose compression level (0-8) [8]: {Colors.ENDC}").strip()
                if level == '':
                    options['compression_level'] = 8
                    break
                level = int(level)
                if 0 <= level <= 8:
                    options['compression_level'] = level
                    break
                else:
                    self.print_warning("Please enter a number between 0 and 8")
            except ValueError:
                self.print_warning("Please enter a valid number")
        
        # Metadata
        options['keep_metadata'] = self.yes_no_prompt("\nPreserve metadata (artist, album, title, etc.)?", default=True)
        
        # Artwork
        options['keep_artwork'] = self.yes_no_prompt("Preserve embedded artwork/album covers?", default=True)
        
        # Delete originals
        options['delete_originals'] = self.yes_no_prompt("\n⚠️  Delete original files after successful conversion?", default=False)
        
        if options['delete_originals']:
            self.print_warning("Original files will be PERMANENTLY DELETED after conversion!")
            if not self.yes_no_prompt("Are you absolutely sure?", default=False):
                options['delete_originals'] = False
                self.print_info("Original files will be kept")
        
        # Output directory
        options['output_subdir'] = self.yes_no_prompt("\nCreate 'FLAC' subdirectory for output files?", default=False)
        
        # Fix permissions
        options['fix_permissions'] = self.yes_no_prompt("Set output files to 777 permissions?", default=True)
        
        return options
    
    def convert_file(self, file_info, options):
        """Convert a single file to FLAC"""
        filepath = file_info['path']
        filename = file_info['filename']
        info = file_info['info']
        
        # Determine output path
        if options['output_subdir']:
            self.output_dir = os.path.join(self.current_dir, 'FLAC')
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Set permissions on the output directory immediately
            if options['fix_permissions']:
                self.fix_permissions(self.output_dir)
        else:
            self.output_dir = self.current_dir
        
        # Create output filename
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(self.output_dir, f"{base_name}.flac")
        
        # Check if output already exists
        if os.path.exists(output_path):
            self.print_warning(f"Output file already exists: {os.path.basename(output_path)}")
            if not self.yes_no_prompt("Overwrite?", default=False):
                return False
        
        # Build ffmpeg command
        cmd_parts = ['ffmpeg', '-i', f'"{filepath}"']
        
        # Map audio stream
        cmd_parts.extend(['-map', '0:a:0'])
        
        # Set FLAC codec and compression
        cmd_parts.extend(['-c:a', 'flac'])
        cmd_parts.extend(['-compression_level', str(options['compression_level'])])
        
        # Handle artwork/video streams
        if options['keep_artwork'] and info['has_video']:
            cmd_parts.extend(['-map', '0:v:0?', '-c:v', 'copy'])
        
        # Handle metadata
        if options['keep_metadata']:
            cmd_parts.extend(['-map_metadata', '0'])
        else:
            cmd_parts.extend(['-map_metadata', '-1'])
        
        # Output file
        cmd_parts.append(f'"{output_path}"')
        
        # Overwrite without asking
        cmd_parts.insert(1, '-y')
        
        cmd = ' '.join(cmd_parts)
        
        # Execute conversion
        self.print_info(f"Converting: {filename}")
        
        returncode, stdout, stderr = self.run_command(cmd, capture_output=True)
        
        if returncode == 0:
            # Set permissions if requested
            if options['fix_permissions']:
                self.fix_permissions(output_path)
            
            # Get output file size
            output_size = os.path.getsize(output_path)
            input_size = os.path.getsize(filepath)
            
            size_diff = ((output_size - input_size) / input_size) * 100
            
            self.print_success(f"Converted: {os.path.basename(output_path)}")
            print(f"  Input:  {input_size / 1024 / 1024:.2f} MB")
            print(f"  Output: {output_size / 1024 / 1024:.2f} MB ({size_diff:+.1f}%)")
            
            # Delete original if requested
            if options['delete_originals']:
                try:
                    os.remove(filepath)
                    self.print_warning(f"  Deleted original: {filename}")
                except Exception as e:
                    self.print_error(f"  Could not delete original: {e}")
            
            return True
        else:
            self.print_error(f"Failed to convert: {filename}")
            if stderr:
                print(f"{Colors.FAIL}{stderr[:500]}{Colors.ENDC}")
            self.conversion_stats['errors'].append(filename)
            return False
    
    def convert_all(self):
        """Convert all files"""
        if not self.files_to_convert:
            self.print_warning("No files to convert")
            return
        
        # Show summary
        self.show_summary()
        
        # Confirm
        if not self.yes_no_prompt("\nProceed with conversion?", default=True):
            self.print_info("Conversion cancelled")
            return
        
        # Get options
        options = self.get_conversion_options()
        
        # Convert
        self.print_header(f"Converting {len(self.files_to_convert)} File(s)")
        
        success_count = 0
        
        for i, file_info in enumerate(self.files_to_convert, 1):
            print(f"\n{Colors.BOLD}[{i}/{len(self.files_to_convert)}]{Colors.ENDC}")
            if self.convert_file(file_info, options):
                success_count += 1
        
        # Fix permissions one final time on the entire output directory
        if options.get('fix_permissions') and self.output_dir:
            self.print_info("\nApplying final permissions fix...")
            if self.fix_permissions_recursive(self.output_dir):
                self.print_success("All permissions set to 777")
        
        # Final summary
        self.print_header("Conversion Complete")
        self.print_success(f"Successfully converted: {success_count}/{len(self.files_to_convert)}")
        
        if self.conversion_stats['errors']:
            self.print_error(f"Failed: {len(self.conversion_stats['errors'])}")
            for f in self.conversion_stats['errors']:
                print(f"  • {f}")
    
    def run(self):
        """Main workflow"""
        self.print_header("Audio to FLAC Converter")
        
        # Check for ffmpeg/ffprobe
        returncode, _, _ = self.run_command("which ffmpeg")
        if returncode != 0:
            self.print_error("ffmpeg is not installed")
            self.print_info("Install with: apt install ffmpeg")
            return
        
        # Scan directory
        if not self.scan_directory():
            return
        
        # Convert
        self.convert_all()

def main():
    """Entry point"""
    try:
        converter = AudioConverter()
        converter.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Operation cancelled by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
