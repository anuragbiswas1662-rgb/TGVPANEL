import re

NEW = '''def stream_vm_console_events(vm_id):
    """Stream serial console output from the VM's QEMU log file."""
    vm = get_vm_by_id(vm_id)
    if not vm:
        yield 'data: {"status": "not_found"}\\n\\n'
        return

    log_path = get_vm_console_log_path(vm_id)
    position = log_path.stat().st_size if log_path.exists() else 0
    last_ping = time.time()

    while True:
        try:
            if log_path.exists():
                with open(log_path, 'rb') as fh:
                    fh.seek(position)
                    chunk = fh.read()
                if chunk:
                    payload = chunk.decode('utf-8', errors='replace')
                    yield f'data: {json.dumps(payload)}\\n\\n'
                    position += len(chunk)
            else:
                if time.time() - last_ping > 10:
                    yield 'data: {"status": "waiting"}\\n\\n'
                    last_ping = time.time()
            time.sleep(0.5)
        except Exception:
            yield 'data: {"status": "disconnected"}\\n\\n'
            break
'''

p = 'hvm.py'
s = open(p, encoding='utf-8').read()
pat = r"def stream_vm_console_events\(vm_id\):.*?(?=\ndef restart_vm_runtime)"
s, n = re.subn(pat, lambda m: NEW.rstrip() + "\n\n", s, count=1, flags=re.DOTALL)
print("replaced", n)
if n:
    open(p, 'w', encoding='utf-8').write(s)
