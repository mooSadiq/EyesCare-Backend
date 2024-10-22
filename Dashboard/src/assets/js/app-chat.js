import { fetchAllData, submitRequest } from './api.js';
const chatHistoryBody = document.querySelector('.chat-history-body');
function scrollToBottom() {
  chatHistoryBody.scrollTo(0, chatHistoryBody.scrollHeight);
}
scrollToBottom();
let otherUserId;
const profileImage = localStorage.getItem('user_profile_picture');

const pusher = new Pusher('6c5bc3a240a5017e7aac', {
  cluster: 'ap1',
  encrypted: true
});


function subscribeToConversation(conversationId) {
  const channel = pusher.subscribe(`conversation-${conversationId}`);
  console.log(channel);
  channel.bind('pusher:subscription_succeeded', function() {
    console.log('Subscribed successfully to the channel.');
  });
  channel.bind('new-message', async function(data) {
    console.log('New message received:', data.message);
    renderNewMessage(data.message); 
  });
}

function renderNewMessage(message) {
  const chatHistory = document.getElementById('chat-history');
  const messageItem = document.createElement('li');
  console.log('first:',otherUserId);
  if (message.sender.id !== otherUserId) {
    // messageItem.className = 'chat-message chat-message-right';
    // messageItem.innerHTML = `
    //   <div class="d-flex overflow-hidden">
    //     <div class="chat-message-wrapper flex-grow-1">
    //       <div class="chat-message-text">
    //       ${
    //         message.file !== null
    //           ? `
    //             <img src="${message.file.file}" alt="Image" width="120" height="150"" />
    //             ${
    //               message.content !== null
    //                 ? `<p class="mb-0">${message.content}</p>`  
    //                 : ' ' 
    //             }
    //           `
    //           : `<p class="mb-0">${message.content}</p>` 
    //       }
    //       </div>
    //       <div class="text-end text-muted mt-1">
    //         <i class="ti ti-checks ti-xs me-1 text-success"></i>
    //         <small>${new Date(message.timestamp).toLocaleTimeString()}</small>
    //       </div>
    //     </div>
    //     <div class="user-avatar flex-shrink-0 ms-3">
    //       <div class="avatar avatar-sm">
    //         <img src="${'../../assets/img/avatars/1.png'}" alt="Avatar" class="rounded-circle" />
    //       </div>
    //     </div>
    //   </div>
    // `;
  } else {
    // رسالة المستخدم الآخر (الرسالة على اليسار)
    messageItem.className = 'chat-message';
    messageItem.innerHTML = `
      <div class="d-flex overflow-hidden">
        <div class="user-avatar flex-shrink-0 me-3">
          <div class="avatar avatar-sm">
            <img src="${message.sender.profile_picture || '/static/img/avatars/default_profile_picture.png'}" alt="Avatar" class="rounded-circle" />
          </div>
        </div>
        <div class="chat-message-wrapper flex-grow-1">
          <div class="chat-message-text">
          ${
            message.file !== null
              ? `
                <img src="${message.file}" alt="Image" width="120" height="150" class="chat-image" />
                ${
                  message.content !== null
                    ? `<p class="mb-0">${message.content}</p>`  
                    : ' ' 
                }
              `
              : `<p class="mb-0">${message.content}</p>` 
          }
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

function initializeData(data) {
  const chatList = document.getElementById('chat-list');
  const contactList = document.getElementById('contact-list');
  const users = data.users;
  const usersWithConversations = data.users.filter(user => user.last_message !== null);
  console.log('chats:', usersWithConversations);
  const usersWithoutConversations = data.users.filter(user => user.last_message === null);
  chatList.innerHTML = '';
  usersWithConversations.forEach(chat => {
      console.log('chat',chat);
      const li = document.createElement('li');
      li.classList.add('chat-contact-list-item');
      const name = chat.first_name +' ' + chat.last_name;
      const chatIdd = chat.last_message.conversation;
      console.log(chatIdd);
      li.innerHTML = `
          <a class="d-flex align-items-center chat-contact-item" href="javascript:void(0);" data-id="${chat.id}" data-name="${name}" data-avatar="${chat.profile_picture}" data-email="${chat.email}">
              <div class="flex-shrink-0 avatar avatar-online'}">
                  <img src="${chat.profile_picture || '/static/img/avatars/default_profile_picture.png'}" alt="Avatar" class="rounded-circle" />
              </div>
              <div class="chat-contact-info flex-grow-1 ms-2">
                  <h6 class="chat-contact-name text-truncate m-0">${name}</h6>
                  <p class="chat-contact-status text-muted text-truncate mb-0">${chat.last_message.content ? chat.last_message.content : "ملف"}</p>
              </div>
              <small class="text-muted mb-auto">${chat.last_message.timestamp}</small>
          </a>
      `;

      li.addEventListener('click', () => {
        updateChatHeader(chat);
        addMessagesToChat(chatIdd);
        scrollToBottom();
      });
      chatList.appendChild(li);
  });

  usersWithoutConversations.forEach(user => {
      const li  = document.createElement('li');
      li.classList.add('chat-contact-list-item');
      const name = user.first_name +' ' + user.last_name;
      li.innerHTML = `
          <a class="d-flex align-items-center">
              <div class="flex-shrink-0 avatar avatar-online'}">
                  <img src="${user.profile_picture || '/static/img/avatars/default_profile_picture.png'}" alt="Avatar" class="rounded-circle" />
              </div>
              <div class="chat-contact-info flex-grow-1 ms-2">
                  <h6 class="chat-contact-name text-truncate m-0">${name}</h6>
                  <p class="chat-contact-status text-muted text-truncate mb-0">${user.email}</p>
              </div>
          </a>
      `;
    li.addEventListener('click', () => {
      updateChatHeader(user);
      otherUserId = user.id;
      startChatWithUser(user.id);
    });
      contactList.appendChild(li);
  });
}

// دالة لتحديث الـ Header الخاص بالشات
function updateChatHeader(user) {
  const chatHeader = document.getElementById('dots-header-actions');
  const userAvatar = document.getElementById('chat-user-avatar');
  const userName = document.getElementById('chat-user-name');
  const userEmail = document.getElementById('chat-user-email');

  // تحديث الصورة والاسم والبريد الإلكتروني
  userAvatar.src = user.profile_picture || '/static/img/avatars/default_profile_picture.png';
  userName.textContent = `${user.first_name} ${user.last_name}`;
  userEmail.textContent = user.email;
  const chatHistory = document.getElementById('chat-history');
  chatHistory.innerHTML = '';
  // إظهار الـ Header والشات
  chatHeader.classList.remove('d-none');
  userAvatar.classList.remove('d-none');
  document.getElementById('chat-history-footer').classList.remove('d-none');
}

async function addMessagesToChat(chatId) {
  const url_get_chat_data = `/chat/api/conversations/${chatId}/`;
  try {
    const conversationData = await fetchAllData(url_get_chat_data);
    console.log(conversationData);
    const chatHistory = document.getElementById('chat-history');
    chatHistory.innerHTML = '';
    otherUserId = conversationData.other_user.id;
    const otherUserprofile_picture = conversationData.other_user.profile_picture;
  
    conversationData.messages.forEach(message => {
      const messageItem = document.createElement('li');
  
      if (message.sender !== otherUserId) {
        messageItem.className = 'chat-message chat-message-right';
        messageItem.innerHTML = `
        <div class="d-flex overflow-hidden">
          <div class="chat-message-wrapper flex-grow-1">
            <div class="chat-message-text">
            ${
              message.file !== null
                ? `
                  <img src="${message.file}" alt="Image" width="120" height="150"" />
                  ${
                    message.content !== null
                      ? `<p class="mb-0">${message.content}</p>`  
                      : ' ' 
                  }
                `
                : `<p class="mb-0">${message.content}</p>` 
            }
            </div>
            <div class="text-end text-muted mt-1">
              <i class="ti ti-checks ti-xs me-1 text-success"></i>
              <small>${new Date(message.timestamp).toLocaleTimeString()}</small>
            </div>
          </div>
          <div class="user-avatar flex-shrink-0 ms-3">
            <div class="avatar avatar-sm">
              <img src="${profileImage || '/static/img/avatars/default_profile_picture.png'}" alt="Avatar" class="rounded-circle" />
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
                <img src="${otherUserprofile_picture || '/static/img/avatars/default_profile_picture.png'}" alt="Avatar" class="rounded-circle" />
              </div>
            </div>
            <div class="chat-message-wrapper flex-grow-1">
              <div class="chat-message-text">
              ${
                message.file !== null
                  ? `
                    <img src="${message.file}" alt="Image" width="120" height="150" class="chat-image rounded-2" />
                    ${
                      message.content !== null
                        ? `<p class="mb-0">${message.content}</p>`  
                        : ' ' 
                    }
                  `
                  : `<p class="mb-0">${message.content}</p>` 
              }
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

      
      
    });
    subscribeToConversation(chatId);
  } catch (error) {
    console.error('خطأ في جلب :', error);
  }
}
console.log(otherUserId);

async function fetchAndInitializeData() {
  const url_get_users_data = '/chat/contacts/';
  try {
      const data = await fetchAllData(url_get_users_data);
      initializeData(data);
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
  const fileInput = document.getElementById('attach-doc').files[0];
    if (messageInput.value || fileInput) {
    const messageContent = messageInput.value;

    const messageItem = document.createElement('li');
    messageItem.className = 'chat-message chat-message-right';
    messageItem.innerHTML = `
    <div class="d-flex overflow-hidden">
      <div class="chat-message-wrapper flex-grow-1">
        <div class="chat-message-text">
        ${
          fileInput? `<img src="${fileInput}" alt="Image" width="120" height="150"" />
              ${
                messageContent !== null
                  ? `<p class="mb-0">${messageContent}</p>`  
                  : ' ' 
              }
            `
            : `<p class="mb-0">${messageContent}</p>` 
        }
        </div>
        <div class="text-end text-muted mt-1">
          <i class="ti ti-clock ti-xs me-1 text-success" id="status-icon"></i>
          <small>${new Date().toLocaleTimeString()}</small>
        </div>
      </div>
      <div class="user-avatar flex-shrink-0 ms-3">
        <div class="avatar avatar-sm">
          <img src="${profileImage || '/static/img/avatars/default_profile_picture.png'}" alt="Avatar" class="rounded-circle" />
        </div>
      </div>
    </div>
  `;

    document.getElementById('chat-history').appendChild(messageItem);
    messageInput.value = '';

    scrollToBottom();
    const method = 'POST';
    const formData = new FormData();
    formData.append('content', messageContent);
    console.log(otherUserId);
    formData.append('receiver', otherUserId);    
    if (fileInput) {
        formData.append('file', fileInput);
    }
    try {
      const url = '/chat/api/conversations/send/';
      const result = await submitRequest(url, method, formData);      
      if (result.success) {
        console.log('تم إرسال الرسالة بنجاح:');
        const statusIcon = messageItem.querySelector('#status-icon');
        if (statusIcon) {
          statusIcon.className = 'ti ti-checks ti-xs me-1 text-success';
        }
        messageInput.value = '';
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

'use strict';

document.addEventListener('DOMContentLoaded',
 function () {
  
  (function () {
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
