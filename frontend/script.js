
// ========== 工具 ==========

function sanitize(dirty) {
    return DOMPurify.sanitize(dirty, { ALLOWED_TAGS: ['b', 'i', 'u', 'p'] });
}

function formatTime(time) {
    const date = new Date(time);
    const pad = n => n.toString().padStart(2, '0');
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}


// ========== 后端API ==========

const API = "https://gift-windbell-uno.onrender.com"

async function getMsgs() {
    const res = await fetch(`${API}/msgs/`);
    return res;
}

async function createMsg(author, title, content) {
    const res = await fetch(`${API}/msgs/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({author, title, content}),  // 字面量简写
    });
    return res;
}


// ========== 显示 ==========

// 1. 获取消息列表元素
const msgList = document.getElementById('msgList');

// 2. 定义显示消息列表函数
async function showMsgs() {
    try {
        const msgs = await (await getMsgs()).json();
        let html = '';
        for (const msg of msgs) {
            html += `<li class="msg">
                <p class="msg-author">${sanitize(msg.author)}</p>
                <p class="msg-title">${sanitize(msg.title)}</p>
                <p class="msg-content">${sanitize(msg.content)}</p>
                <p class="msg-time">${formatTime(msg.created_at)}</p>
            </li>`;
        }
        msgList.innerHTML = html;
    } catch (error) {
        msgList.innerHTML = '<div class="error-message">❌️获取消息失败</div>';
        console.error(error);
    }
}

// 3. 调用显示消息列表函数
showMsgs();


// ========== 输入 ==========

// 1. 获取按钮和输入框元素
const submitBtn = document.getElementById('submitBtn');
const authorInput = document.getElementById('author');
const titleInput = document.getElementById('title');
const contentTextarea = document.getElementById('content');

// 2. 定义提交处理函数
async function handleSubmit() {
    const author = authorInput.value.trim();
    const title = titleInput.value.trim();
    const content = contentTextarea.value.trim();

    if (!author) {
        alert('请输入作者');
        return;
    }
    if (!title || !content) {
        alert('请填写完整信息');
        return;
    }
    if (author.length > 20 && title.length > 50 && content.length > 250) {
        alert('作者、标题和内容分别不能超过20、50和250个字符');
        return;
    }
    
    const res = await createMsg(author, title, content);

    if (res.ok)  {
        alert('提交成功');
        showMsgs();
        titleInput.value = '';
        contentTextarea.value = '';
        titleInput.focus();
    } else {
        alert(`提交失败 ${res.status}`);
        console.error(res);
    }
}

// 3. 绑定点击事件
submitBtn.addEventListener('click', handleSubmit);
