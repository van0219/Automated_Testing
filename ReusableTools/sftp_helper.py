# -*- coding: utf-8 -*-
"""
SFTP Helper Module

Reusable SFTP operations for FSM interface testing.
Handles file uploads, downloads, and evidence generation for TES-070 documentation.

Usage:
    from sftp_helper import upload_file, download_file, load_sftp_credentials
    
    creds = load_sftp_credentials('Projects/StateOfNewHampshire/Credentials/')
    result = upload_file('test.csv', '/Infor_FSM/Inbound/', creds)
"""

import paramiko
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_sftp_credentials(credentials_folder: str, server_name: Optional[str] = None) -> Dict[str, str]:
    """
    Load SFTP credentials from server-specific file or .env.passwords.
    
    Args:
        credentials_folder: Path to credentials folder (e.g., 'Projects/StateOfNewHampshire/Credentials/')
        server_name: Optional server name (e.g., 'Tamics10_AX1', 'ACUITY_TST')
                    If provided, looks for {server_name}.sftp file first
    
    Returns:
        Dictionary with SFTP connection details
    
    Raises:
        FileNotFoundError: If credentials file doesn't exist
        ValueError: If required credentials are missing
    """
    creds_path = Path(credentials_folder)
    
    # Try server-specific file first if server_name provided
    if server_name:
        server_file = creds_path / f'{server_name}.sftp'
        if server_file.exists():
            logger.info(f"📁 Using server-specific credentials: {server_file}")
            creds_file = server_file
        else:
            logger.info(f"⚠️ Server-specific file not found: {server_file}, falling back to .env.passwords")
            creds_file = creds_path / '.env.passwords'
    else:
        creds_file = creds_path / '.env.passwords'
    
    if not creds_file.exists():
        raise FileNotFoundError(f"Credentials file not found: {creds_file}")
    
    credentials = {}
    required_keys = ['SFTP_HOST', 'SFTP_PORT', 'SFTP_USERNAME', 'SFTP_PASSWORD']
    
    with open(creds_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                if key in required_keys or key.startswith('SFTP_'):
                    credentials[key] = value
    
    # Validate required credentials
    missing = [key for key in required_keys if key not in credentials]
    if missing:
        raise ValueError(f"Missing required SFTP credentials: {', '.join(missing)}")
    
    # Convert port to integer
    credentials['SFTP_PORT'] = int(credentials['SFTP_PORT'])
    
    logger.info(f"✅ Loaded SFTP credentials from {creds_file}")
    return credentials


def upload_file(local_file: str, remote_path: str, credentials: Dict[str, str]) -> Dict[str, any]:
    """
    Upload a file to SFTP server.
    
    Args:
        local_file: Path to local file to upload
        remote_path: Remote directory path (e.g., '/Infor_FSM/Inbound/')
        credentials: SFTP credentials dictionary from load_sftp_credentials()
    
    Returns:
        Dictionary with upload details for evidence generation
    
    Raises:
        FileNotFoundError: If local file doesn't exist
        Exception: If upload fails
    """
    local_path = Path(local_file)
    
    if not local_path.exists():
        raise FileNotFoundError(f"Local file not found: {local_file}")
    
    # Prepare remote file path
    filename = local_path.name
    remote_file = remote_path.rstrip('/') + '/' + filename
    
    # Get file info
    file_size = local_path.stat().st_size
    upload_time = datetime.now()
    
    logger.info(f"📤 Uploading {filename} to {credentials['SFTP_HOST']}{remote_file}")
    
    try:
        # Connect to SFTP
        transport = paramiko.Transport((credentials['SFTP_HOST'], credentials['SFTP_PORT']))
        transport.connect(username=credentials['SFTP_USERNAME'], password=credentials['SFTP_PASSWORD'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Upload file
        sftp.put(str(local_path), remote_file)
        
        # Close connection
        sftp.close()
        transport.close()
        
        logger.info(f"✅ Upload successful: {filename}")
        
        return {
            'success': True,
            'filename': filename,
            'local_path': str(local_path),
            'remote_path': remote_file,
            'server': credentials['SFTP_HOST'],
            'file_size': file_size,
            'upload_time': upload_time.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': upload_time
        }
        
    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}")
        raise Exception(f"SFTP upload failed: {str(e)}")


def download_file(remote_file: str, local_path: str, credentials: Dict[str, str]) -> Dict[str, any]:
    """
    Download a file from SFTP server.
    
    Args:
        remote_file: Remote file path (e.g., '/Infor_FSM/Outbound/output.csv')
        local_path: Local path to save file
        credentials: SFTP credentials dictionary
    
    Returns:
        Dictionary with download details for evidence generation
    
    Raises:
        Exception: If download fails
    """
    local_file = Path(local_path)
    local_file.parent.mkdir(parents=True, exist_ok=True)
    
    download_time = datetime.now()
    
    logger.info(f"📥 Downloading {remote_file} from {credentials['SFTP_HOST']}")
    
    try:
        # Connect to SFTP
        transport = paramiko.Transport((credentials['SFTP_HOST'], credentials['SFTP_PORT']))
        transport.connect(username=credentials['SFTP_USERNAME'], password=credentials['SFTP_PASSWORD'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Download file
        sftp.get(remote_file, str(local_file))
        
        # Get file size
        file_size = local_file.stat().st_size
        
        # Close connection
        sftp.close()
        transport.close()
        
        logger.info(f"✅ Download successful: {local_file.name}")
        
        return {
            'success': True,
            'filename': local_file.name,
            'remote_path': remote_file,
            'local_path': str(local_file),
            'server': credentials['SFTP_HOST'],
            'file_size': file_size,
            'download_time': download_time.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': download_time
        }
        
    except Exception as e:
        logger.error(f"❌ Download failed: {str(e)}")
        raise Exception(f"SFTP download failed: {str(e)}")


def list_remote_files(remote_path: str, credentials: Dict[str, str]) -> List[str]:
    """
    List files in a remote SFTP directory.
    
    Args:
        remote_path: Remote directory path
        credentials: SFTP credentials dictionary
    
    Returns:
        List of filenames in the directory
    """
    logger.info(f"📋 Listing files in {remote_path}")
    
    try:
        transport = paramiko.Transport((credentials['SFTP_HOST'], credentials['SFTP_PORT']))
        transport.connect(username=credentials['SFTP_USERNAME'], password=credentials['SFTP_PASSWORD'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        files = sftp.listdir(remote_path)
        
        sftp.close()
        transport.close()
        
        logger.info(f"✅ Found {len(files)} files")
        return files
        
    except Exception as e:
        logger.error(f"❌ List files failed: {str(e)}")
        raise Exception(f"SFTP list files failed: {str(e)}")


def file_exists(remote_file: str, credentials: Dict[str, str]) -> bool:
    """
    Check if a file exists on SFTP server.
    
    Args:
        remote_file: Remote file path
        credentials: SFTP credentials dictionary
    
    Returns:
        True if file exists, False otherwise
    """
    try:
        transport = paramiko.Transport((credentials['SFTP_HOST'], credentials['SFTP_PORT']))
        transport.connect(username=credentials['SFTP_USERNAME'], password=credentials['SFTP_PASSWORD'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        try:
            sftp.stat(remote_file)
            exists = True
        except FileNotFoundError:
            exists = False
        
        sftp.close()
        transport.close()
        
        return exists
        
    except Exception as e:
        logger.error(f"❌ File exists check failed: {str(e)}")
        return False


def generate_upload_evidence_html(upload_result: Dict[str, any], output_dir: str) -> str:
    """
    Generate HTML evidence page for SFTP upload (for screenshot).
    
    Args:
        upload_result: Result dictionary from upload_file()
        output_dir: Directory to save HTML file
    
    Returns:
        Path to generated HTML file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    html_file = output_path / 'sftp_upload_evidence.html'
    
    # Format file size
    size_kb = upload_result['file_size'] / 1024
    size_str = f"{size_kb:.2f} KB" if size_kb < 1024 else f"{size_kb/1024:.2f} MB"
    
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SFTP Upload Evidence</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 700px;
            margin: 0 auto;
        }}
        .success-icon {{
            color: #2ecc71;
            font-size: 64px;
            text-align: center;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #2c3e50;
            margin: 0 0 30px 0;
            text-align: center;
            font-size: 28px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        td {{
            padding: 15px;
            border-bottom: 1px solid #ecf0f1;
        }}
        td:first-child {{
            font-weight: 600;
            color: #7f8c8d;
            width: 180px;
        }}
        td:last-child {{
            color: #2c3e50;
        }}
        .status {{
            display: inline-block;
            padding: 6px 16px;
            background: #2ecc71;
            color: white;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #95a5a6;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="success-icon">✅</div>
        <h2>SFTP Upload Successful</h2>
        <table>
            <tr>
                <td>File Name:</td>
                <td><strong>{upload_result['filename']}</strong></td>
            </tr>
            <tr>
                <td>SFTP Server:</td>
                <td>{upload_result['server']}</td>
            </tr>
            <tr>
                <td>Remote Path:</td>
                <td>{upload_result['remote_path']}</td>
            </tr>
            <tr>
                <td>File Size:</td>
                <td>{size_str} ({upload_result['file_size']:,} bytes)</td>
            </tr>
            <tr>
                <td>Upload Time:</td>
                <td>{upload_result['upload_time']}</td>
            </tr>
            <tr>
                <td>Status:</td>
                <td><span class="status">✓ Completed</span></td>
            </tr>
        </table>
        <div class="footer">
            Generated by FSM Test Automation Framework
        </div>
    </div>
</body>
</html>'''
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"📄 Generated upload evidence: {html_file}")
    return str(html_file)


def generate_download_evidence_html(download_result: Dict[str, any], output_dir: str) -> str:
    """
    Generate HTML evidence page for SFTP download (for screenshot).
    
    Args:
        download_result: Result dictionary from download_file()
        output_dir: Directory to save HTML file
    
    Returns:
        Path to generated HTML file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    html_file = output_path / 'sftp_download_evidence.html'
    
    # Format file size
    size_kb = download_result['file_size'] / 1024
    size_str = f"{size_kb:.2f} KB" if size_kb < 1024 else f"{size_kb/1024:.2f} MB"
    
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SFTP Download Evidence</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            padding: 40px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            margin: 0;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 700px;
            margin: 0 auto;
        }}
        .success-icon {{
            color: #3498db;
            font-size: 64px;
            text-align: center;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #2c3e50;
            margin: 0 0 30px 0;
            text-align: center;
            font-size: 28px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        td {{
            padding: 15px;
            border-bottom: 1px solid #ecf0f1;
        }}
        td:first-child {{
            font-weight: 600;
            color: #7f8c8d;
            width: 180px;
        }}
        td:last-child {{
            color: #2c3e50;
        }}
        .status {{
            display: inline-block;
            padding: 6px 16px;
            background: #3498db;
            color: white;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #95a5a6;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="success-icon">📥</div>
        <h2>SFTP Download Successful</h2>
        <table>
            <tr>
                <td>File Name:</td>
                <td><strong>{download_result['filename']}</strong></td>
            </tr>
            <tr>
                <td>SFTP Server:</td>
                <td>{download_result['server']}</td>
            </tr>
            <tr>
                <td>Remote Path:</td>
                <td>{download_result['remote_path']}</td>
            </tr>
            <tr>
                <td>Local Path:</td>
                <td>{download_result['local_path']}</td>
            </tr>
            <tr>
                <td>File Size:</td>
                <td>{size_str} ({download_result['file_size']:,} bytes)</td>
            </tr>
            <tr>
                <td>Download Time:</td>
                <td>{download_result['download_time']}</td>
            </tr>
            <tr>
                <td>Status:</td>
                <td><span class="status">✓ Completed</span></td>
            </tr>
        </table>
        <div class="footer">
            Generated by FSM Test Automation Framework
        </div>
    </div>
</body>
</html>'''
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"📄 Generated download evidence: {html_file}")
    return str(html_file)
