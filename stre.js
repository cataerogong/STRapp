// ------------------------------------------------
// Module <STRapp>
// ------------------------------------------------
class SettingGroupSTRapp extends SettingGroupBase {
	constructor() {
		super("STRapp", "STRapp 单机模式");
		this.add(new SettingText("books", "书籍目录", "/books"));
		this.add(new SettingText("progress", "阅读进度目录", "/progress"));
		this.add(new SettingCheckbox("sortByStatus", "按阅读状态分类排序（在读，未读，读完）", true));
	}

	genHTML() {
		let html = `<div id="${this.full_id}" class="setting-group"><div class="sub-cap">${this.desc}</div>
            <div class="setting-group-settings">
            ${this.get("books").genLabelElm()} ${this.get("books").genInputElm()}
            ${this.get("progress").genLabelElm()} ${this.get("progress").genInputElm()}
            <div class="row">${this.get("sortByStatus").genInputElm()} ${this.get("sortByStatus").genLabelElm()}</div>
            `;
		return html;
	}

	apply() {
		STRapp.booksDir = this.get("books").value.trimEnd().replace(/\/*$/, "");
		STRapp.progressDir = this.get("progress").value.trimEnd().replace(/\/*$/, "");
        STRapp.sortByStatus = this.get("sortByStatus").value;
        STRapp.refreshBookList();
	}
}

var STRapp = {
	booksDir: "", // "/books"
	progressDir: "", // "/progress"
	sortByStatus: false,
	syncInterval: 300, // 同步间隔（ms）

	async openBook(fname) {
		showLoadingScreen();
		// STReHelper.fetchLink(this.booksDir + "/" + fname).then((resp) => {
        webui_call_func("get_book_data", this.booksDir + "/" + fname).then((data) => {
                let f = new File([data], fname, { type: "text/plain" });
                resetVars();
                handleSelectedFile([f]);
		}).catch((e) => {
			console.log(e);
			alert("打开书籍出错");
			resetUI();
		});
	},

	async getProgress(name) {
		return await webui_call_func("get_progress", this.progressDir + "/" + name + ".progress");
	},

	async setProgress(name, progress) {
		return await webui_call_func("set_progress", this.progressDir + "/" + name + ".progress", progress);
	},

	async saveProgress() {
		if (filename) {
			if (contentContainer.style.display == "none") { // 阅读区域不可见，说明可能正在drag，getTopLineNumber()会取到错误行数，应该跳过
				return;
			}
			let line = getHistory(filename, false); // getCurLineNumber();
			if ((filename + ":" + line) != this.STReFileLine) {
				// console.log("Save progress on server: " + filename + ":" + line + "/" + fileContentChunks.length);
				try {
					await this.setProgress(filename, line + "/" + (fileContentChunks.length - 1));
                    this.updateBookProgressInfo(this.getBookProgress(filename));
				} catch (e) {
					console.log(e);
				}
				this.STReFileLine = filename + ":" + line;
			}
		}
	},

	async loadProgress() {
		if (filename) {
			// console.log("Check progress on server: " + filename);
			try {
				let progress = await STRapp.getProgress(filename);
				let m = STRe_PROGRESS_RE.exec(progress);
				if (m) { // 取到服务端进度
					let line = parseInt(m.groups["line"]);
					let curLine = getCurLineNumber();
					if (line == curLine) { // 进度一致，无需同步
						STRapp.STReFileLine = filename + ":" + line;
					} else { // 进度不一致
                        console.log("Load progress on server: " + filename + ":" + progress);
                        setHistory(filename, line);
                        getHistory(filename);
                        STRapp.STReFileLine = filename + ":" + line;
					}
				}
			} catch (e) {
				console.log(e);
			}
		}
	},

	// 更新书籍封面的阅读进度
	updateBookProgressInfo(bookInfo, bookElm = null) {
		if (!bookElm) {
			bookElm = $(`.bookshelf .book[data-filename="${bookInfo.filename}"]`);
			if (bookElm.length <= 0) {
				return;
			}
		}
		if (bookInfo.read) {
			bookElm.addClass("read").css("--read-progress", bookInfo.pct);
			bookElm.find(".progress").html(bookInfo.pct).attr("title", `${bookInfo.pct} (${bookInfo.progress})`);
		} else {
			bookElm.removeClass("read").css("--read-progress", "");
 			bookElm.find(".progress").html("&nbsp;").attr("title", "");
		}
		if (bookInfo.completed) {
			bookElm.addClass("completed");
		} else {
			bookElm.removeClass("completed");
		}
	},

	async getBookProgress(fname) {
		let ret = {filename: fname, progress: "", pct: "", read: false, completed: false};
		// ret.progress = STReHelper.getLocalProgress(fname);
		ret.progress = await this.getProgress(fname);
		if (ret.progress) {
			ret.read = true;
			ret.pct = "?%";
			let m = STRe_PROGRESS_RE.exec(ret.progress);
			if (m && m.groups["total"]) {
				ret.pct = ((m.groups["line"] / m.groups["total"]) * 100).toFixed(1) + "%";
				ret.completed = (m.groups["line"] == m.groups["total"]);
			}
		}
		return ret;
	},

	genBookItem(bookInfo) {
		let book = $(`<div class="book ${bookInfo.isEastern ? "eastern" : ""}" data-filename="${bookInfo.filename}">
			<div class="cover" title="${bookInfo.filename}">
				<div class="bookname">${bookInfo.bookname}</div>
				<div class="author">${bookInfo.author}</div>
			</div>
			<div class="info">
				<div class="size">${(bookInfo.size/1000/1000).toFixed(2)} MB</div>
				<div class="progress"></div>
			</div></div>`);
		book.find(".cover").click((evt) => {
			evt.originalEvent.stopPropagation();
			this.openBook(bookInfo.filename);
		});
		this.updateBookProgressInfo(bookInfo, book);
		return book;
	},

	async refreshBookList() {
		/**
		 * 调整封面字体大小
		 * @param {HTMLElement} bookElm 必须已加入 DOM Tree
		 */
		function resizeFont(bookElm) {
			let b = $(bookElm).find(".cover")[0];
			let s = parseInt(window.getComputedStyle(b).fontSize.slice(0, -2));
			while ((b.scrollHeight > b.offsetHeight || b.scrollWidth > b.offsetWidth) && s > 12) {
				b.style.setProperty("--cover-font-size", (--s) + "px")
			}
		}

        let container = $(".bookshelf .book-list");
        container.html("");
        let booklist = [];
        try {
            for (const book of await webui_call_func("get_all_books", this.booksDir)) {
                let na = getBookNameAndAuthor(book.name.replace(/(.txt)$/i, ''));
                // booklist.push({filename: book.name, bookname: na.bookName, author: na.author, size: book.data.size});
                let info = await this.getBookProgress(book.name);
                info.bookname = na.bookName;
                info.author = na.author;
                info.size = book.size;
                // info.isEastern = getLanguage(info.bookname);
                booklist.push(info);
            }
            if (this.sortByStatus)
                booklist.sort((a, b) => {
                    if (a.completed != b.completed) return (a.completed - b.completed);
                    if (a.read != b.read) return (b.read - a.read);
                    return (a.bookname.localeCompare(b.bookname, "zh"));
                });
            else
                booklist.sort((a, b) => (a.bookname.localeCompare(b.bookname, "zh")));
            for (const bookInfo of booklist) {
                let book = this.genBookItem(bookInfo).css("visibility", "hidden");
                container.append(book);
                resizeFont(book);
                book.css("visibility", "visible");
            }
        } catch (e) {
            console.log(e);
            container.html(e);
        }
	},

	async show() {
        $(`<div class="bookshelf">
            <div class="title">本地书架</div>
            <span class="book-list"></span>
            </div>`).appendTo("#dropZone");
        $(`<div class="btn-icon" style="margin-left:10px;width:1.5rem;height:1.5rem;border-radius:5px;display:inline-flex;">
			<svg class="icon" style="width:1rem;height:1rem;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
				<path fill="none" stroke="none" d="M24 0v24H0V0zM12.594 23.258l-.012.002l-.071.035l-.02.004l-.014-.004l-.071-.036c-.01-.003-.019 0-.024.006l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427c-.002-.01-.009-.017-.016-.018m.264-.113l-.014.002l-.184.093l-.01.01l-.003.011l.018.43l.005.012l.008.008l.201.092c.012.004.023 0 .029-.008l.004-.014l-.034-.614c-.003-.012-.01-.02-.02-.022m-.715.002a.023.023 0 0 0-.027.006l-.006.014l-.034.614c0 .012.007.02.017.024l.015-.002l.201-.093l.01-.008l.003-.011l.018-.43l-.003-.012l-.01-.01z"/><path fill="currentColor" d="M20 9.5a1.5 1.5 0 0 1 1.5 1.5a8.5 8.5 0 0 1-8.5 8.5h-2.382a1.5 1.5 0 0 1-2.179 2.06l-2.494-2.494a1.495 1.495 0 0 1-.445-1.052v-.028c.003-.371.142-.71.368-.97l.071-.077l2.5-2.5a1.5 1.5 0 0 1 2.18 2.061H13a5.5 5.5 0 0 0 5.5-5.5A1.5 1.5 0 0 1 20 9.5m-4.44-7.06l2.5 2.5a1.5 1.5 0 0 1 0 2.12l-2.5 2.5a1.5 1.5 0 0 1-2.178-2.06H11A5.5 5.5 0 0 0 5.5 13a1.5 1.5 0 1 1-3 0A8.5 8.5 0 0 1 11 4.5h2.382a1.5 1.5 0 0 1 2.179-2.06"/>
            </svg></div>`)
            .click(async () => await this.refreshBookList())
            .appendTo(".bookshelf .title");
        await this.refreshBookList();
	},

	async loop() { // 定时同步进度
        localStorage.setItem(this.STRe_FILENAME, filename);
        await this.saveProgress();
        setTimeout(() => this.loop(), this.syncInterval);
	},
	pauseLoop() {
		STRapp.loopPaused = true;
	},
	resumeLoop() {
		STRapp.loopPaused = false;
	},

    async init() {
        fileloadCallback.regBefore(this.pauseLoop);
        fileloadCallback.regAfter(this.loadProgress);
        fileloadCallback.regAfter(this.resumeLoop);
        await this.show();
        console.log("Module <STRapp> loaded.");
        setTimeout(() => this.loop(), this.syncInterval);

        settingMgr.add(new SettingGroupSTRapp());
    }
};

STRapp.init();
