function toggleSidebar() {
    document.body.classList.toggle('sidebar-open');
    let overlay = document.getElementById('sidebarOverlay');

    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'sidebarOverlay';
        overlay.className = 'sidebar-overlay hidden';
        overlay.onclick = toggleSidebar;
        document.body.appendChild(overlay);
    }

    overlay.classList.toggle('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('sidebarOverlay')) {
        const overlay = document.createElement('div');
        overlay.id = 'sidebarOverlay';
        overlay.className = 'sidebar-overlay hidden';
        overlay.onclick = toggleSidebar;
        document.body.appendChild(overlay);
    }
});
