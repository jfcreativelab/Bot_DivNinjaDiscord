document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('lead-form');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = form.name.value.trim();
    const email = form.email.value.trim();
    if (!name || !email) {
      alert('Preencha todos os campos!');
      return;
    }
    alert(`Obrigado, ${name}! Em breve entraremos em contato através do e-mail: ${email}`);
    form.reset();
  });
});
