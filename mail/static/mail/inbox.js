document.addEventListener('DOMContentLoaded', function() {

	console.log("done")

	// Use buttons to toggle between views
	document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'))
	document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'))
	document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'))
	document.querySelector('#compose').addEventListener('click', () => compose_email());

	// When form is submitted
	document.querySelector("#compose-form").addEventListener('submit', submit_email);

	// When view email button is clicked

	// By default, load the inbox
	load_mailbox('inbox')
});

function compose_email(_recipients="", subject="", body="", reply_intro="") {

	// Show compose view and hide other views
	document.querySelector('#emails-view').style.display = 'none'
	document.querySelector('#compose-view').style.display = 'block'
	document.querySelector('#email-view').style.display = 'none'

	// Clear out composition fields
	console.log(_recipients)
	document.querySelector('#compose-recipients').value = _recipients
	if (subject.includes("Re: ") || subject === "") {
		document.querySelector('#compose-subject').value = subject
	} else {
		document.querySelector('#compose-subject').value = "Re: "+subject
	}
	document.querySelector('#compose-body').value = "\n"+reply_intro+"\n"+body
}

function submit_email() {
	const recipients = document.querySelector("#compose-recipients").value
	const subject = document.querySelector("#compose-subject").value
	const body = document.querySelector("#compose-body").value

	console.log(recipients)
	console.log(subject)
	console.log(body)

	fetch('/emails', {
		method: 'POST',
		body: JSON.stringify({
			"recipients": recipients,
			"subject": subject,
			"body": body
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print result
		console.log("updated")
		console.log(result)
	})
	
  return false
}

function load_mailbox(mailbox) {
	
	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'block'
	document.querySelector('#compose-view').style.display = 'none'
	document.querySelector('#email-view').style.display = 'none'

	// Show mailbox name
	document.querySelector('#emails-view').innerHTML = `
	<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`

	// Get emails, display them, and create 'click' event
	fetch('/emails/'+mailbox)
	.then(response => response.json())
	.then(emails => {
		// Print email
		// console.log(emails);
		emails.forEach(function(email, index) {
			// document.querySelector('#emails-view').innerHTML += display_condensedMail(email)
		
			const element = document.createElement('div');
			if (email.read === true) {
				element.setAttribute("class", "card border-secondary bg-light")
			} else {
				element.setAttribute("class", "card border-secondary")
			}
			element.innerHTML = display_condensedMail(email)
			element.addEventListener('click', () => viewMail(email.id)) // Create event
			document.querySelector('#emails-view').append(element)
		})
	})
}

function viewMail(id) {
  
	// Show the mailbox and hide other views
	document.querySelector('#emails-view').style.display = 'none'
	document.querySelector('#compose-view').style.display = 'none'
	document.querySelector('#email-view').style.display = 'block'
	
	fetch("emails/"+id)
	.then(response => response.json())
	.then(email => {
		//Clear existing HTML
		document.querySelector('#email-view').innerHTML = ""
		
		const element = document.createElement('div');
		element.innerHTML = display_Mail(email)
		// Button for replying
		element.querySelector("#reply").addEventListener('click', () => compose_email(
			email.sender, email.subject, email.body,
			`On ${email.timestamp} ${email.sender} wrote:`
		))
		// Button for archiving/unarchiving
		element.querySelector("#archive").addEventListener('click', (event) => archive(email.id, event.target.value))
		document.querySelector('#email-view').append(element)
		
		console.log(email)
		markAs_Read(email.id, 1)
	})
}

function markAs_Read(id, read) {
	fetch('/emails/'+id, {
		method: 'PUT',
		body: JSON.stringify({
			"read": read
		})
	})
	
	console.log('marked as read')
}

function reply(id) {
	fds
}

function archive(id, archive) {
	console.log(id)
	console.log(archive)
	
	fetch('/emails/'+id, {
		method: 'PUT',
		body: JSON.stringify({
			"archived": archive
		})
	})
	console.log(true)
	// Reload the page
	viewMail(id)
}

function display_condensedMail(email) {

	divContent = `
	<div class="card-body">
		<b>${email.sender}</b> &nbsp;&nbsp;&nbsp;&nbsp; ${email.subject}
		<p class="d-inline float-right">${email.timestamp}</p>
	</div>`

  return divContent
}

function display_Mail(email) {
	if (email.archived === false) {
		btn_name = "Archive"
		final_archive_param = 1
	} else {
		btn_name = "Unarchive"
		final_archive_param = 0
	}
	
	divContent = `
	<b>From:</b> ${email.sender}<br>
	<b>To:</b> ${email.recipients.toString()}<br>
	<b>Subject:</b> ${email.subject}<br>
	<b>Timestamp:</b> ${email.timestamp}<br>
	<button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
	<button class="btn btn-sm btn-outline-secondary" id="archive" value="${final_archive_param}">${btn_name}</button>
	<hr>
	${email.body}
	`
	return divContent
}