
// ========== 工具 ==========

function sanitize(dirty) {
    return DOMPurify.sanitize(dirty, { ALLOWED_TAGS: ['b', 'i', 'u', 'p'] });
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
    return res.ok;
}


// ========== 显示 ==========

// 1. 获取消息列表元素
const msgList = document.getElementById('msgList');

// 2. 定义显示消息列表函数
async function showMsgs() {
    try {
        const res = await getMsgs();
    } catch (error) {
        msgList.innerHTML = '<div class="error-message">❌️获取消息失败</div>';
        return;
    }
    let html = '';
    for (const msg of res.json()) {
        html += `<li class="msg">
            <p class="author">${sanitize(msg.author)}</p>
            <p class="title">${sanitize(msg.title)}</p>
            <p class="content">${sanitize(msg.content)}</p>
            <p class="time">${sanitize(msg.created_at)}</p>
            </li>`;
    }
    msgList.innerHTML = html;
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
    
    const success = await createMsg(author, title, content);

    if (success)  showMsgs();
    else  alert('提交失败');
}

// 3. 绑定点击事件
submitBtn.addEventListener('click', handleSubmit);
