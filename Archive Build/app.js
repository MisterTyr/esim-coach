// Simple filter by region
document.querySelectorAll('.filters button').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('.filters button').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.getAttribute('data-filter');
    document.querySelectorAll('#grid .card').forEach(card=>{
      const region = card.getAttribute('data-region');
      card.style.display = (f==='all'||f===region)?'block':'none';
    });
  });
});
