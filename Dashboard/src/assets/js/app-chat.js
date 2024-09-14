import { fetchAllData, submitRequest } from './api.js';
const chatHistoryBody = document.querySelector('.chat-history-body');
function scrollToBottom() {
  chatHistoryBody.scrollTo(0, chatHistoryBody.scrollHeight);
}
scrollToBottom();
const pusher = new Pusher('6c5bc3a240a5017e7aac', {
  cluster: 'ap1',
  encrypted: true
});
const chatHistoryHeader = document.getElementById('chat-history-header');
const chatHistoryFooter = document.getElementById('chat-history-footer');
const userAvatarElement = document.getElementById('user-avatar');
const userNameElement = document.getElementById('user-name');
const userEmailElement = document.getElementById('user-email');
console.log(pusher);

// دالة للاشتراك في المحادثة
function subscribeToConversation(conversationId) {
  const channel = pusher.subscribe(`conversation-${conversationId}`);
  console.log(channel);
  // التأكد من الاشتراك بنجاح
  channel.bind('pusher:subscription_succeeded', function() {
    console.log('Subscribed successfully to the channel.');
  });
  // استقبال الرسائل الجديدة
  channel.bind('new-message', function(data) {
    console.log('New message received:', data.message);
    renderNewMessage(data.message); // قم بإضافة الرسالة إلى واجهة المستخدم
  });
}

// دالة لإضافة الرسائل الجديدة إلى واجهة المستخدم
function renderNewMessage(message) {
  const chatHistory = document.getElementById('chat-history');

  const messageItem = document.createElement('li');

  if (message.sender !== otherUserId) {
    messageItem.className = 'chat-message chat-message-right';
    messageItem.innerHTML = `
      <div class="d-flex overflow-hidden">
        <div class="chat-message-wrapper flex-grow-1">
          <div class="chat-message-text">
            <p class="mb-0">${message.content}</p>
          </div>
          <div class="text-end text-muted mt-1">
            <i class="ti ti-checks ti-xs me-1 text-success"></i>
            <small>${new Date(message.timestamp).toLocaleTimeString()}</small>
          </div>
        </div>
        <div class="user-avatar flex-shrink-0 ms-3">
          <div class="avatar avatar-sm">
            <img src="${'../../assets/img/avatars/1.png'}" alt="Avatar" class="rounded-circle" />
          </div>
        </div>
      </div>
    `;
  } else {
    messageItem.className = 'chat-message';
    messageItem.innerHTML = `
      <div class="d-flex overflow-hidden">
        <div class="user-avatar flex-shrink-0 me-3">
          <div class="avatar avatar-sm">
            <img src="${message.sender_profile_picture || '../../assets/img/avatars/2.png'}" alt="Avatar" class="rounded-circle" />
          </div>
        </div>
        <div class="chat-message-wrapper flex-grow-1">
          <div class="chat-message-text">
            <p class="mb-0">${message.content}</p>
          </div>
          <div class="text-muted mt-1">
            <small>${new Date(message.timestamp).toLocaleTimeString()}</small>
          </div>
        </div>
      </div>
    `;
  }

  chatHistory.appendChild(messageItem);
  scrollToBottom();

}

function initializeChatData(data) {
  const contactList = document.getElementById('chat-list');

  contactList.innerHTML = '';
  console.log(data)
  data.forEach(chat => {
      const li = document.createElement('li');
      li.classList.add('chat-contact-list-item');
      const name = chat.other_user.first_name +' ' + chat.other_user.last_name;
      li.innerHTML = `
          <a class="d-flex align-items-center chat-contact-item" href="javascript:void(0);" data-id="${chat.id}" data-name="${name}" data-avatar="${chat.other_user.profile_picture}" data-email="${chat.other_user.email}">
              <div class="flex-shrink-0 avatar avatar-online'}">
                  <img src="${chat.other_user.profile_picture || '../../assets/img/avatars/default-avatar.png'}" alt="Avatar" class="rounded-circle" />
              </div>
              <div class="chat-contact-info flex-grow-1 ms-2">
                  <h6 class="chat-contact-name text-truncate m-0">${name}</h6>
                  <p class="chat-contact-status text-muted text-truncate mb-0">${chat.last_message.content}</p>
              </div>
              <small class="text-muted mb-auto">${chat.last_message.time_since}</small>
          </a>
      `;
      contactList.appendChild(li);
  });
  document.querySelectorAll('.chat-contact-item').forEach(link => {
    link.addEventListener('click', function () {
        const chatId = parseInt(this.getAttribute('data-id'), 10);
        const userName = this.getAttribute('data-name');
        const userEmail = this.getAttribute('data-email');
        const userAvatar = this.getAttribute('data-avatar');
        if (!isNaN(chatId)) {
          userNameElement.innerText = userName;
          userEmailElement.innerText = userEmail;
          userAvatarElement.src = userAvatar;
          chatHistoryHeader.classList.remove('d-none');
          chatHistoryFooter.classList.remove('d-none');
          addMessagesToChat(chatId);
          console.log(chatId);
        }
    });
});
}
function initializeData(data) {
  // الحصول على العنصر <ul> الذي يحتوي على قائمة المستخدمين
  const contactList = document.getElementById('contact-list');

  // تفريغ أي محتويات سابقة
  // contactList.innerHTML = '';
  console.log(data.users)
  // تكرار لكل مستخدم في البيانات
  data.users.forEach(user => {
      // إنشاء عنصر <li> جديد
      const li = document.createElement('li');
      li.classList.add('chat-contact-list-item');
      const name = user.first_name +' ' + user.last_name;
      // إضافة محتوى المستخدم داخل <li>
      li.innerHTML = `
          <a class="d-flex align-items-center">
              <div class="flex-shrink-0 avatar avatar-online'}">
                  <img src="${user.profile_picture || '../../assets/img/avatars/default-avatar.png'}" alt="Avatar" class="rounded-circle" />
              </div>
              <div class="chat-contact-info flex-grow-1 ms-2">
                  <h6 class="chat-contact-name text-truncate m-0">${name}</h6>
                  <p class="chat-contact-status text-muted text-truncate mb-0">${user.email}</p>
              </div>
          </a>
      `;

      // إضافة عنصر <li> إلى القائمة
      contactList.appendChild(li);
  });
}
let otherUserId = null;
async function addMessagesToChat(chatId) {
  const url_get_chat_data = `/api/chat/conversations/${chatId}`;
  try {
    const conversationData = await fetchAllData(url_get_chat_data);
    console.log(conversationData);
    const chatHistory = document.getElementById('chat-history');
    chatHistory.innerHTML = '';
    otherUserId = conversationData.other_user.id;
    const otherUserprofile_picture = conversationData.other_user.profile_picture;
  
    conversationData.messages.forEach(message => {
      // إنشاء عنصر الرسالة
      const messageItem = document.createElement('li');
  
      // تحديد التنسيق حسب المرسل
      if (message.sender !== otherUserId) {
        // رسالة المستخدم الحالي (الرسالة على اليمين)
        messageItem.className = 'chat-message chat-message-right';
        messageItem.innerHTML = `
          <div class="d-flex overflow-hidden">
            <div class="chat-message-wrapper flex-grow-1">
              <div class="chat-message-text">
                <p class="mb-0">${message.content}</p>
              </div>
              <div class="text-end text-muted mt-1">
                <i class="ti ti-checks ti-xs me-1 text-success"></i>
                <small>${new Date(message.timestamp).toLocaleTimeString()}</small>
              </div>
            </div>
            <div class="user-avatar flex-shrink-0 ms-3">
              <div class="avatar avatar-sm">
                <img src="${ '../../assets/img/avatars/1.png'}" alt="Avatar" class="rounded-circle" />
              </div>
            </div>
          </div>
        `;
      } else {
        // رسالة المستخدم الآخر (الرسالة على اليسار)
        messageItem.className = 'chat-message';
        messageItem.innerHTML = `
          <div class="d-flex overflow-hidden">
            <div class="user-avatar flex-shrink-0 me-3">
              <div class="avatar avatar-sm">
                <img src="${otherUserprofile_picture || '../../assets/img/avatars/2.png'}" alt="Avatar" class="rounded-circle" />
              </div>
            </div>
            <div class="chat-message-wrapper flex-grow-1">
              <div class="chat-message-text">
                <p class="mb-0">${message.content}</p>
              </div>
              <div class="text-muted mt-1">
                <small>${new Date(message.timestamp).toLocaleTimeString()}</small>
              </div>
            </div>
          </div>
        `;
      }
  
      // إضافة الرسالة إلى قائمة الرسائل
      chatHistory.appendChild(messageItem);
      scrollToBottom();

      
      

    });
    subscribeToConversation(chatId);
  } catch (error) {
    console.error('خطأ في جلب :', error);
  }
}
console.log(otherUserId);
// استدعاء الدالة بعد جلب بيانات المحادثة

async function fetchAndInitializeData() {
  const url_get_users_data = '/chat/api/get/users/';
  try {
      const data = await fetchAllData(url_get_users_data);
      initializeData(data);
  } catch (error) {
      console.error('خطأ في جلب بيانات :', error);
  }
}

async function fetchConv() {
  const url_get_users_data = '/chat/api/get/conv/';
  try {
      const data = await fetchAllData(url_get_users_data);
      initializeChatData(data);
  } catch (error) {
      console.error('خطأ في جلب بيانات :', error);
  }
  
}
const formSendMessage = document.querySelector('.form-send-message');
const messageInput = document.querySelector('.message-input');
// Send Message
formSendMessage.addEventListener('submit', async (e) => {
  e.preventDefault();
  console.log(otherUserId);
  const otheruserId = otherUserId;
  console.log(otheruserId);
  if (messageInput.value) {
    // الحصول على الرسالة
    const messageContent = messageInput.value;

    // // إنشاء عنصر جديد للرسالة المرسلة
    // const messageItem = document.createElement('li');
    // messageItem.className = 'chat-message chat-message-right';
    // messageItem.innerHTML = `
    //   <div class="d-flex overflow-hidden">
    //     <div class="chat-message-wrapper flex-grow-1">
    //       <div class="chat-message-text">
    //         <p class="mb-0 text-break">${messageContent}</p>
    //       </div>
    //       <div class="text-end text-muted mt-1">
    //         <i class="ti ti-checks ti-xs me-1 text-success"></i>
    //         <small>${new Date().toLocaleTimeString()}</small>
    //       </div>
    //     </div>
    //     <div class="user-avatar flex-shrink-0 ms-3">
    //       <div class="avatar avatar-sm">
    //         <img src="${'../../assets/img/avatars/1.png'}" alt="Avatar" class="rounded-circle" />
    //       </div>
    //     </div>
    //   </div>
    // `;

    // // إضافة الرسالة إلى قائمة الرسائل
    // document.getElementById('chat-history').appendChild(messageItem);

    // إعادة تعيين حقل الإدخال
    messageInput.value = '';

    // التمرير إلى الأسفل
    // scrollToBottom();
    const method = 'POST';
    const formData = new FormData();
    formData.append('content', messageContent);
    console.log(otherUserId);
    formData.append('receiver', otherUserId);
    // هنا يمكنك إرسال الرسالة إلى السيرفر إذا كنت ترغب في حفظها
    try {
      const url = '/api/chat/messages/send/';
      const result = await submitRequest(url, method, formData);      
      if (result.success) {
        console.log('تم إرسال الرسالة بنجاح:');
        scrollToBottom();

      }
      else {
        console.log('فشل ارسال الرسالة ')
      }
    } catch (error) {
      console.error('خطأ أثناء إرسال الرسالة:', error);
    }
  }
});
// Initialize on page load

'use strict';

document.addEventListener('DOMContentLoaded',
 function () {
  
  (function () {
    fetchConv();
    fetchAndInitializeData();
    const chatContactsBody = document.querySelector('.app-chat-contacts .sidebar-body'),
      chatContactListItems = [].slice.call(
        document.querySelectorAll('.chat-contact-list-item:not(.chat-contact-list-item-title)')
      ),
      chatHistoryBody = document.querySelector('.chat-history-body'),
      chatSidebarLeftBody = document.querySelector('.app-chat-sidebar-left .sidebar-body'),
      chatSidebarRightBody = document.querySelector('.app-chat-sidebar-right .sidebar-body'),
      chatUserStatus = [].slice.call(document.querySelectorAll(".form-check-input[name='chat-user-status']")),
      chatSidebarLeftUserAbout = $('.chat-sidebar-left-user-about'),

      searchInput = document.querySelector('.chat-search-input'),
      userStatusObj = {
        active: 'avatar-online',
        offline: 'avatar-offline',
        away: 'avatar-away',
        busy: 'avatar-busy'
      };

    // Initialize PerfectScrollbar
    // ------------------------------

    // Chat contacts scrollbar
    if (chatContactsBody) {
      new PerfectScrollbar(chatContactsBody, {
        wheelPropagation: false,
        suppressScrollX: true
      });
    }

    // Chat history scrollbar
    if (chatHistoryBody) {
      new PerfectScrollbar(chatHistoryBody, {
        wheelPropagation: false,
        suppressScrollX: true
      });
    }

    // Sidebar left scrollbar
    if (chatSidebarLeftBody) {
      new PerfectScrollbar(chatSidebarLeftBody, {
        wheelPropagation: false,
        suppressScrollX: true
      });
    }

    // Sidebar right scrollbar
    if (chatSidebarRightBody) {
      new PerfectScrollbar(chatSidebarRightBody, {
        wheelPropagation: false,
        suppressScrollX: true
      });
    }

    // Scroll to bottom function
    function scrollToBottom() {
      chatHistoryBody.scrollTo(0, chatHistoryBody.scrollHeight);
    }
    scrollToBottom();

    // User About Maxlength Init
    if (chatSidebarLeftUserAbout.length) {
      chatSidebarLeftUserAbout.maxlength({
        alwaysShow: true,
        warningClass: 'label label-success bg-success text-white',
        limitReachedClass: 'label label-danger',
        separator: '/',
        validate: true,
        threshold: 120
      });
    }

    // Update user status
    chatUserStatus.forEach(el => {
      el.addEventListener('click', e => {
        let chatLeftSidebarUserAvatar = document.querySelector('.chat-sidebar-left-user .avatar'),
          value = e.currentTarget.value;
        //Update status in left sidebar user avatar
        chatLeftSidebarUserAvatar.removeAttribute('class');
        Helpers._addClass('avatar avatar-xl ' + userStatusObj[value] + '', chatLeftSidebarUserAvatar);
        //Update status in contacts sidebar user avatar
        let chatContactsUserAvatar = document.querySelector('.app-chat-contacts .avatar');
        chatContactsUserAvatar.removeAttribute('class');
        Helpers._addClass('flex-shrink-0 avatar ' + userStatusObj[value] + ' me-3', chatContactsUserAvatar);
      });
    });

    // Select chat or contact
    chatContactListItems.forEach(chatContactListItem => {
      // Bind click event to each chat contact list item
      chatContactListItem.addEventListener('click', e => {
        // Remove active class from chat contact list item
        chatContactListItems.forEach(chatContactListItem => {
          chatContactListItem.classList.remove('active');
        });
        // Add active class to current chat contact list item
        e.currentTarget.classList.add('active');
      });
    });

    // Filter Chats
    if (searchInput) {
      searchInput.addEventListener('keyup', e => {
        let searchValue = e.currentTarget.value.toLowerCase(),
          searchChatListItemsCount = 0,
          searchContactListItemsCount = 0,
          chatListItem0 = document.querySelector('.chat-list-item-0'),
          contactListItem0 = document.querySelector('.contact-list-item-0'),
          searchChatListItems = [].slice.call(
            document.querySelectorAll('#chat-list li:not(.chat-contact-list-item-title)')
          ),
          searchContactListItems = [].slice.call(
            document.querySelectorAll('#contact-list li:not(.chat-contact-list-item-title)')
          );

        // Search in chats
        searchChatContacts(searchChatListItems, searchChatListItemsCount, searchValue, chatListItem0);
        // Search in contacts
        searchChatContacts(searchContactListItems, searchContactListItemsCount, searchValue, contactListItem0);
      });
    }

    // Search chat and contacts function
    function searchChatContacts(searchListItems, searchListItemsCount, searchValue, listItem0) {
      searchListItems.forEach(searchListItem => {
        let searchListItemText = searchListItem.textContent.toLowerCase();
        if (searchValue) {
          if (-1 < searchListItemText.indexOf(searchValue)) {
            searchListItem.classList.add('d-flex');
            searchListItem.classList.remove('d-none');
            searchListItemsCount++;
          } else {
            searchListItem.classList.add('d-none');
          }
        } else {
          searchListItem.classList.add('d-flex');
          searchListItem.classList.remove('d-none');
          searchListItemsCount++;
        }
      });
      // Display no search fount if searchListItemsCount == 0
      if (searchListItemsCount == 0) {
        listItem0.classList.remove('d-none');
      } else {
        listItem0.classList.add('d-none');
      }
    }



    // on click of chatHistoryHeaderMenu, Remove data-overlay attribute from chatSidebarLeftClose to resolve overlay overlapping issue for two sidebar
    let chatHistoryHeaderMenu = document.querySelector(".chat-history-header [data-target='#app-chat-contacts']"),
      chatSidebarLeftClose = document.querySelector('.app-chat-sidebar-left .close-sidebar');
    chatHistoryHeaderMenu.addEventListener('click', e => {
      chatSidebarLeftClose.removeAttribute('data-overlay');
    });
    // }


  })();
});
