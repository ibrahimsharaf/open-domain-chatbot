

function chat(msg)
{
    retyp(msg);
}

function clearContent()
{
if (confirm('Are you sure you want to clear the chat?')) {
    document.getElementById("message1").value='';
    }
}


function getReply()
{
//elmafrod btnady 3al chatbot w tedelo el msg w tgeb el answer
chat('Bot: answer');

}