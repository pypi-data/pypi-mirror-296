{{ ! template('head', title='') }}

	<div id="bonus-info">
		<table id="workdirs">
			% for workdir in sorted(workdirs):
				<tr>
					<td><a target="_blank" href="/workdir/{{ url_quote(workdir) }}">{{ workdir }}</a></td>
					<td><a target="_blank" href="/job/{{ url_quote(workdir) }}-LATEST">latest</a></td>
				</tr>
			% end
			<tr>
				<td><a target="_blank" href="/workdir/">ALL</a></td>
			</tr>
		</table>
		<ul>
			<li><a target="_blank" href="/methods">methods</a></li>
			<li><a target="_blank" href="/urd">urd</a></li>
		</ul>
		<input type="submit" value="show all" id="show-all" disabled>
	</div>
	<h1 id="header">
		ax board: {{ project }}
		<span id="path">{{ path[8:] }}</span>
	</h1>
	<div id="status">
		<a target="_blank" href="/status">status</a>: <span></span>
	</div>
	<div id="dirs"><ul></ul></div>
	<div id="missing"></div>
	<div id="waiting"><div class="spinner"></div></div>
<script language="javascript">
(function () {
	const imageExts = new Set(['jpg', 'jpeg', 'gif', 'png', 'apng', 'svg', 'bmp', 'webp']);
	const videoExts = new Set(['mp4', 'mov', 'mpg', 'mpeg', 'mkv', 'avi', 'webm']);
	const waitingEl = document.getElementById('waiting');
	const statusEl = document.querySelector('#status span');
	const show_all = document.getElementById('show-all');
	show_all.onclick = function() {
		show_all.disabled = true;
		for (const el of document.querySelectorAll('.result.hidden')) {
			el.classList.remove('hidden');
		}
	}
	const status = function () {
		if (document.body.className === 'error') {
			setTimeout(status, 1500);
			return;
		}
		fetch('/status?short', {headers: {Accept: 'text/plain'}})
		.then(res => {
			if (res.ok) return res.text();
			throw new Error('error response');
		})
		.then(res => {
			statusEl.innerText = res;
			setTimeout(status, 1500);
		})
		.catch(error => {
			console.log(error);
			statusEl.innerText = '???';
			setTimeout(status, 1500);
		});
	};
	const update = function (try_num) {
		fetch('{{ url_path }}', {headers: {Accept: 'application/json'}})
		.then(res => {
			if (res.ok) return res.json();
			throw new Error('error response');
		})
		.then(res => {
			const missing = document.getElementById('missing');
			if (res.missing) {
				missing.className = 'error';
				missing.innerText = res.missing
			} else {
				missing.className = '';
			}
			const existing = {};
			for (const el of document.querySelectorAll('.result')) {
				if (el.dataset.name) existing[el.dataset.name] = el;
			};

			const dirs_ul = document.querySelector('#dirs ul');
			const dirs_els = {};
			for (const el of dirs_ul.querySelectorAll('li')) {
				dirs_els[el.dataset.name] = el;
				el.remove();
			}
			const dirs = Object.entries(res.dirs).sort();
			for (const [name, href] of dirs) {
				let el = dirs_els[name];
				if (!el) {
					el = document.createElement('LI');
					el.dataset.name = name;
					const a = document.createElement('A');
					a.innerText = name;
					a.href = encodeURI(href);
					el.appendChild(a);
				}
				dirs_ul.appendChild(el);
			}

			const items = Object.entries(res.files);
			if (items.length) {
				waitingEl.style.display = 'none';
			} else {
				waitingEl.style.display = 'block';
			}
			// sort files on ts, but fall back to (link) name for files with the same time
			items.sort((a, b) => b[1].ts - a[1].ts || a[0].localeCompare(b[0]));
			let prev = waitingEl;
			for (const [name, data] of items) {
				const oldEl = existing[name];
				if (oldEl) {
					delete existing[name];
					if (oldEl.dataset.ts == data.ts) {
						update_date(oldEl);
						prev = oldEl;
						continue;
					}
					remove(oldEl);
				}
				const resultEl = document.createElement('DIV');
				const txt = text => resultEl.appendChild(document.createTextNode(text));
				const a = function (text, ...parts) {
					const a = document.createElement('A');
					a.innerText = text;
					let href = '/job'
					for (const part of parts) {
						href = href + '/' + encodeURIComponent(part);
					}
					a.href = href;
					a.target = '_blank';
					resultEl.appendChild(a);
				}
				resultEl.className = 'result';
				resultEl.dataset.name = name;
				resultEl.dataset.ts = data.ts;
				if (data.jobid) {
					a(name, data.jobid, data.name);
					txt(' from ');
					a(data.jobid, data.jobid);
					txt(' (');
					const methodEl = document.createElement('SPAN')
					methodEl.className = 'method'
					resultEl.appendChild(methodEl);
					txt(')');
					fetch('/job/' + encodeURIComponent(data.jobid), {headers: {Accept: 'application/json'}})
					.then(res => {
						if (res.ok) return res.json();
						throw new Error('error response');
					})
					.then(res => {
						const a = document.createElement('A');
						a.innerText = res.params.method;
						a.href = '/method/' + encodeURIComponent(res.params.method);
						a.target = '_blank';
						methodEl.appendChild(a);
					});
				} else {
					txt(name + ' ');
					const el = document.createElement('SPAN');
					el.className = 'unknown';
					el.appendChild(document.createTextNode('from UNKNOWN'));
					resultEl.appendChild(el);
				}
				txt(' ');
				const dateEl = document.createElement('SPAN');
				dateEl.className = 'date';
				resultEl.appendChild(dateEl)
				update_date(resultEl);
				const size = document.createElement('INPUT');
				size.type = 'submit';
				size.value = 'big';
				size.disabled = true;
				resultEl.appendChild(size);
				const hide = document.createElement('INPUT');
				hide.type = 'submit';
				hide.value = 'hide';
				hide.onclick = function () {
					show_all.disabled = false;
					resultEl.classList.add('hidden');
				}
				resultEl.appendChild(hide);
				resultEl.appendChild(sizewrap(name, data, size));
				prev.after(resultEl);
				prev = resultEl;
			}
			for (const el of Object.values(existing)) {
				remove(el);
			}
			setTimeout(update, 1500);
		})
		.catch(error => {
			console.log(error);
			if (try_num === 4) {
				document.body.className = 'error';
				waitingEl.style.display = 'none';
				const header = document.getElementById('header');
				const goodHTML = header.innerHTML;
				header.innerText = 'ERROR - updates stopped at ' + fmtdate();
				const btn = document.createElement('INPUT');
				btn.type = 'button';
				btn.value = 'restart';
				btn.id = 'restart';
				btn.onclick = function () {
					document.body.className = '';
					waitingEl.style.display = 'block';
					header.innerHTML = goodHTML;
					update();
				};
				header.appendChild(btn);
			} else {
				waitingEl.style.display = 'block';
				setTimeout(() => update((try_num || 0) + 1), 1500);
			}
		});
	};
	const remove = function (el) {
		if (el.classList.contains('hidden')) {
			el.remove();
		} else {
			setTimeout(el.remove, 1400);
			el.classList.add('hidden');
			el.dataset.name = '';
		}
	};
	const sizewrap = function (name, data, size) {
		if (data.size < 5000000) return load(name, data, size);
		const clickEl = document.createElement('DIV');
		clickEl.className = 'clickme';
		clickEl.innerText = 'Click to load ' + data.size + ' bytes';
		clickEl.onclick = function () {
			clickEl.parentNode.replaceChild(load(name, data, size), clickEl);
		};
		return clickEl;
	};
	const name2ext = function (name) {
		const parts = name.split('.');
		let ext = parts.pop().toLowerCase();
		if (ext === 'gz' && parts.length > 1) {
			ext = parts.pop().toLowerCase();
		}
		return ext;
	}
	const load = function (name, data, size) {
		const fileUrl = '{{ url_path }}/' + encodeURIComponent(name) + '?ts=' + data.ts;
		const ext = name2ext(name);
		const container = document.createElement('DIV');
		const spinner = document.createElement('DIV');
		spinner.className = 'spinner';
		container.appendChild(spinner);
		const onerror = function () {
			spinner.remove();
			container.className = 'error';
			container.innerText = 'ERROR';
		};
		let fileEl;
		let stdhandling = false;
		size.disabled = false;
		size.onclick = function () {
			if (container.className) {
				size.value = 'big';
				container.className = '';
			} else {
				size.value = 'small';
				container.className = 'big';
				container.scrollIntoView({behavior: 'smooth', block: 'end'});
			}
		};
		if (imageExts.has(ext)) {
			fileEl = document.createElement('IMG');
			fileEl.onclick = function () {
				if (fileEl.naturalHeight > fileEl.height) {
					if (container.className) {
						container.className = 'full';
						size.value = 'small';
						fileEl.scrollIntoView({behavior: 'smooth', block: 'nearest'});
					} else {
						container.className = 'big';
						container.scrollIntoView({behavior: 'smooth', block: 'nearest'});
						if (fileEl.naturalHeight > fileEl.height) {
							size.value = 'bigger';
						} else {
							size.value = 'small';
						}
					}
				} else {
					size.value = 'big';
					container.className = '';
					fileEl.className = '';
				}
			};
			size.onclick = fileEl.onclick;
			stdhandling = true;
		} else if (videoExts.has(ext)) {
			fileEl = document.createElement('VIDEO');
			fileEl.src = fileUrl;
			fileEl.controls = true;
			spinner.remove(); // shows a video UI immediately anyway
		} else if (ext === 'pdf') {
			fileEl = document.createElement('EMBED');
			fileEl.type = 'application/pdf';
			stdhandling = true;
		} else {
			fileEl = document.createElement('DIV');
			fileEl.className = 'textfile';
			const pre = document.createElement('PRE');
			fileEl.appendChild(pre);
			fetch(fileUrl, {headers: {Accept: 'text/plain'}})
			.then(res => {
				if (res.ok) return res.text();
				throw new Error('error response');
			})
			.then(res => {
				if (ext === 'html') {
					fileEl.innerHTML = res;
				} else {
					parseANSI(pre, res);
				}
				spinner.remove();
			})
			.catch(error => {
				console.log(error);
				onerror();
			});
		}
		if (stdhandling) {
			fileEl.onload = () => spinner.remove();
			fileEl.onerror = onerror;
			fileEl.src = fileUrl;
		}
		container.appendChild(fileEl);
		return container;
	};
	const update_date = function(el) {
		const date = new Date(el.dataset.ts * 1000);
		el.querySelector('.date').innerText = fmtdate_ago(date);
	};
	const fmtdate = function(date) {
		if (!date) date = new Date();
		return date.toISOString().substring(0, 19).replace('T', ' ') + 'Z';
	};
	const units = [['minute', 60], ['hour', 24], ['day', 365.25], ['year', 0]];
	const fmtdate_ago = function (date) {
		const now = new Date();
		let ago = (now - date) / 60000;
		for (const [unit, size] of units) {
			if (size === 0 || ago < size) {
				ago = ago.toFixed(0);
				let s = (ago == 1) ? '' : 's';
				return fmtdate(date) + ', ' + ago + ' ' + unit + s + ' ago';
			}
			ago = ago / size;
		}
	};
	update();
	status();
})();
</script>
</body>
