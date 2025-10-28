"""
Main Application - Entry point for the testing agent
"""
import yaml
import sys
import argparse
from pathlib import Path
from loguru import logger

from app.emulator_manager import EmulatorManager
from app.apk_installer import APKInstaller
from app.ui_explorer import UIExplorer
from app.test_executor import TestExecutor
from app.report_generator import ReportGenerator

def setup_logging(config):
    """Setup logging configuration"""
    logger.remove()  # Remove default handler
    
    # Console handler
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=config['logging']['level']
    )
    
    # File handler
    logger.add(
        config['logging']['file'],
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level="DEBUG",
        rotation="10 MB"
    )

def load_config(config_path="config/config.yaml"):
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {str(e)}")
        sys.exit(1)

def load_documentation(doc_path):
    """Load app documentation if provided"""
    if not doc_path or not Path(doc_path).exists():
        return None
    
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            documentation = f.read()
        logger.info(f"Documentation loaded from {doc_path}")
        return documentation
    except Exception as e:
        logger.warning(f"Failed to load documentation: {str(e)}")
        return None

def main():
    """Main application entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Automated Mobile App Testing Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --apk myapp.apk
  python main.py --apk myapp.apk --docs app_features.txt
  python main.py --apk myapp.apk --config custom_config.yaml
        """
    )
    
    parser.add_argument(
        '--apk',
        required=True,
        help='Path to APK file to test'
    )
    
    parser.add_argument(
        '--docs',
        help='Path to documentation file (optional)'
    )
    
    parser.add_argument(
        '--config',
        default='config/config.yaml',
        help='Path to configuration file (default: config/config.yaml)'
    )
    
    parser.add_argument(
        '--skip-emulator',
        action='store_true',
        help='Skip emulator startup (use if emulator already running)'
    )
    
    args = parser.parse_args()
    
    # Validate APK path
    if not Path(args.apk).exists():
        logger.error(f"APK file not found: {args.apk}")
        sys.exit(1)
    
    # Load configuration
    config = load_config(args.config)
    setup_logging(config)
    
    logger.info("=" * 60)
    logger.info("🤖 Automated Mobile App Testing Agent")
    logger.info("=" * 60)
    
    # Load documentation
    documentation = load_documentation(args.docs)
    
    # Initialize components
    emulator = EmulatorManager(config)
    apk_installer = APKInstaller(config)
    ui_explorer = UIExplorer(config)
    test_executor = TestExecutor(config, ui_explorer, apk_installer)
    report_generator = ReportGenerator(config)
    
    try:
        # Step 1: Start emulator
        if not args.skip_emulator:
            logger.info("\n📱 Step 1: Starting Android Emulator...")
            if not emulator.start():
                logger.error("Failed to start emulator. Exiting.")
                sys.exit(1)
        else:
            logger.info("\n📱 Step 1: Using existing emulator...")
            if not emulator.is_running():
                logger.error("Emulator not running. Remove --skip-emulator flag.")
                sys.exit(1)
        
        # Step 2: Install APK
        logger.info("\n📦 Step 2: Installing APK...")
        if not apk_installer.install(args.apk):
            logger.error("Failed to install APK. Exiting.")
            emulator.stop()
            sys.exit(1)
        
        # Grant permissions
        apk_installer.grant_permissions()
        
        # Step 3: Run tests
        logger.info("\n🧪 Step 3: Running Automated Tests...")
        test_summary = test_executor.run_tests(documentation)
        
        # Step 4: Generate report
        logger.info("\n📊 Step 4: Generating Test Report...")
        apk_info = {
            'package_name': apk_installer.package_name,
            'main_activity': apk_installer.main_activity,
            'apk_path': args.apk
        }
        
        report_path = report_generator.generate(test_summary, apk_info)
        
        # Display summary
        logger.info("\n" + "=" * 60)
        logger.info("✅ Testing Complete!")
        logger.info("=" * 60)
        logger.info(f"📊 Total Tests: {test_summary['total_tests']}")
        logger.info(f"✅ Passed: {test_summary['passed']}")
        logger.info(f"❌ Failed: {test_summary['failed']}")
        logger.info(f"🖼️  Screens Explored: {test_summary['screens_explored']}")
        logger.info(f"📄 Report: {report_path}")
        logger.info("=" * 60)
        
        # Cleanup
        logger.info("\n🧹 Cleaning up...")
        apk_installer.stop()
        
        if not args.skip_emulator:
            emulator.stop()
        
        logger.info("\n✨ All done! Check the report for detailed results.")
        
    except KeyboardInterrupt:
        logger.warning("\n\n⚠️  Testing interrupted by user")
        apk_installer.stop()
        if not args.skip_emulator:
            emulator.stop()
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"\n❌ An error occurred: {str(e)}")
        logger.exception("Full error details:")
        apk_installer.stop()
        if not args.skip_emulator:
            emulator.stop()
        sys.exit(1)

if __name__ == "__main__":
    main()