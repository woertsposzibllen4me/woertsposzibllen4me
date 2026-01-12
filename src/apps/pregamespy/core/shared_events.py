"""Shared events for PregameSpy application."""

import asyncio

secondary_windows_spawned = asyncio.Event()
"""Event signaling that the windows created by opencv have been spawned and are
ready to be managed."""

mute_ssim_prints = asyncio.Event()
"""Event signaling that SSIM prints to the console should be stopped to give way for
other informative prints."""
