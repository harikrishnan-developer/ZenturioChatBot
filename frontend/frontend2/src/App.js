import React, { useState } from 'react';
import './App.css';
import ChatBox from './ChatBox';
import { FaBars } from 'react-icons/fa';

function App() {
  const [page, setPage] = useState('chat');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleNav = (p) => {
    setPage(p);
    setSidebarOpen(false);
  };

  return (
    <div className="app-layout">
      <div className="topbar">
        <button className="menu-btn" onClick={() => setSidebarOpen(true)}><FaBars /></button>
      </div>
      <aside className={`sidebar-drawer${sidebarOpen ? ' open' : ''}`}
        onClick={() => setSidebarOpen(false)}>
        <div className="sidebar" onClick={e => e.stopPropagation()}>
          <nav>
            <ul>
              <li className={page === 'chat' ? 'active' : ''} onClick={() => handleNav('chat')}>Chat</li>
              <li className={page === 'info' ? 'active' : ''} onClick={() => handleNav('info')}>General Services Info</li>
              <li className={page === 'emergency' ? 'active' : ''} onClick={() => handleNav('emergency')}>Emergency Numbers</li>
            </ul>
          </nav>
        </div>
      </aside>
      <main className="main-content">
        {page === 'chat' && <ChatBox />}
        {page === 'info' && (
          <div className="info-section">
            <h2>General Services Info</h2>
            <p>Below are some of the major services provided by the Kerala government, including certificates, licenses, utility payments, and more. Click the links for official portals and detailed instructions.</p>
            <div className="service-category">
              <h3>Civil Registration (Certificates)</h3>
              <ul>
                <li><b>Birth Certificate Application:</b> Apply online for a child’s birth certificate via <a href="https://ksmart.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Ksmart</a> or <a href="https://cr.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sevana</a>. Used for ID creation, school admission, visas, etc.</li>
                <li><b>Birth Certificate Download:</b> Download an existing birth certificate using the <a href="https://cr.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sevana Civil Registration portal</a>.</li>
                <li><b>Death Certificate Application:</b> Register a death and apply for an official certificate through the Civil Registration Department. <a href="https://cr.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sevana Portal</a>.</li>
                <li><b>Death Certificate Download:</b> Download a registered death certificate online via the <a href="https://cr.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sevana portal</a>.</li>
                <li><b>Marriage Certificate Registration:</b> Register marriages under various acts via the <a href="https://cr.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sevana portal</a>.</li>
                <li><b>Marriage Certificate Download:</b> Download a legally registered marriage certificate from the <a href="https://cr.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sevana portal</a>.</li>
              </ul>
            </div>
            <div className="service-category">
              <h3>Property & Business</h3>
              <ul>
                <li><b>Sanchaya Property Tax:</b> Pay annual property tax online or offline. <a href="https://sanchaya.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sanchaya Portal</a>.</li>
                <li><b>Sanchaya Ownership Certificate:</b> Download official property ownership certificates. <a href="https://sanchaya.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sanchaya Portal</a>.</li>
                <li><b>D&O (Dangerous & Offensive) License:</b> Apply for business licenses required for public health/safety. <a href="https://sanchaya.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sanchaya Portal</a>.</li>
              </ul>
            </div>
            <div className="service-category">
              <h3>Utility Services</h3>
              <ul>
                <li><b>Water, Electricity, Telephone Bill Payment:</b> Pay utility bills online via <a href="https://sanchaya.lsgkerala.gov.in" target="_blank" rel="noopener noreferrer">Sanchaya</a>, <a href="https://wss.kseb.in/selfservices/" target="_blank" rel="noopener noreferrer">KSEB</a>, or <a href="https://epay.kwa.kerala.gov.in/" target="_blank" rel="noopener noreferrer">KWA</a> portals.</li>
                <li><b>KSEB Electricity Bill Payment:</b> Pay Kerala State Electricity Board bills online or offline. <a href="https://wss.kseb.in/selfservices/" target="_blank" rel="noopener noreferrer">KSEB Quick Pay</a>.</li>
                <li><b>Water Bill Payment (Kerala Water Authority):</b> Pay water bills online via <a href="https://epay.kwa.kerala.gov.in/" target="_blank" rel="noopener noreferrer">KWA Quick Pay</a>.</li>
              </ul>
            </div>
            <div className="service-category">
              <h3>Transport & Licenses</h3>
              <ul>
                <li><b>Driving License Renewal:</b> Renew your expired driving license online via <a href="https://parivahan.gov.in/parivahan/" target="_blank" rel="noopener noreferrer">Parivahan</a> or at RTO.</li>
                <li><b>Apply for New Driving License:</b> Apply for a new driving license after passing the Learner's License test. <a href="https://parivahan.gov.in/parivahan/" target="_blank" rel="noopener noreferrer">Parivahan Portal</a>.</li>
                <li><b>Learner’s License Application:</b> Apply for a Learner's License by taking the online test. <a href="https://parivahan.gov.in/parivahan/" target="_blank" rel="noopener noreferrer">Parivahan Portal</a>.</li>
                <li><b>Duplicate Driving License:</b> Get a duplicate DL if the original is lost, stolen, or damaged. <a href="https://parivahan.gov.in/parivahan/" target="_blank" rel="noopener noreferrer">Parivahan Portal</a>.</li>
                <li><b>Change of Address in DL:</b> Update your address on the Driving License. <a href="https://parivahan.gov.in/parivahan/" target="_blank" rel="noopener noreferrer">Parivahan Portal</a>.</li>
                <li><b>International Driving Permit (IDP):</b> Apply for an IDP to drive abroad. <a href="https://parivahan.gov.in/parivahan/" target="_blank" rel="noopener noreferrer">Parivahan Portal</a>.</li>
              </ul>
            </div>
            <div className="service-category">
              <h3>Ration Card & Civil Supplies</h3>
              <ul>
                <li><b>Ration Card Application:</b> Apply for a new Kerala Ration Card for subsidized food grains. <a href="https://civilsupplieskerala.gov.in/" target="_blank" rel="noopener noreferrer">Civil Supplies Portal</a>.</li>
                <li><b>Add/Remove Member to Ration Card:</b> Add or remove family members from your Ration Card. <a href="https://civilsupplieskerala.gov.in/" target="_blank" rel="noopener noreferrer">Civil Supplies Portal</a>.</li>
                <li><b>Ration Card Correction:</b> Correct errors in your Ration Card details. <a href="https://civilsupplieskerala.gov.in/" target="_blank" rel="noopener noreferrer">Civil Supplies Portal</a>.</li>
                <li><b>Ration Card Application Status:</b> Track your Ration Card application status online. <a href="https://etso.civilsupplieskerala.gov.in/index.php/c_check_appl_status" target="_blank" rel="noopener noreferrer">Check Status</a>.</li>
              </ul>
            </div>
            <div className="service-category">
              <h3>Identity & Electoral Services</h3>
              <ul>
                <li><b>Aadhaar Enrolment/Update:</b> Register or update your Aadhaar card at authorized centres or online. <a href="https://uidai.gov.in" target="_blank" rel="noopener noreferrer">UIDAI Portal</a>.</li>
                <li><b>Voter Registration (EPIC):</b> Register as a new voter or update details via Akshaya Centres, CSCs, or online. <a href="https://www.nvsp.in" target="_blank" rel="noopener noreferrer">NVSP Portal</a>.</li>
                <li><b>Voter ID Correction (EPIC Update):</b> Update or correct details in your Voter ID. <a href="https://www.nvsp.in" target="_blank" rel="noopener noreferrer">NVSP Portal</a>.</li>
              </ul>
            </div>
          </div>
        )}
        {page === 'emergency' && (
          <div className="emergency-section">
            <h2>Kerala Government Helplines & Office Contacts</h2>
            <p>Below are important helpline numbers and office contacts for Kerala government services, presented in a clear and professional format.</p>
            <hr />
            <h3>General Administration Department (Secretariat)</h3>
            <ul>
              <li><b>Chief Secretary (GAD):</b> +91 471-2333147, 2518181 | Fax: +91 471-2327176 | E-mail: <a href="mailto:chiefsecy@kerala.gov.in">chiefsecy@kerala.gov.in</a></li>
              <li><b>Additional Chief Secretary (GAD):</b> +91 471-2320311, 2518669 | E-mail: <a href="mailto:secy.gad@kerala.gov.in">secy.gad@kerala.gov.in</a></li>
              <li><b>Secretariat Exchange (PABX):</b> +91 471-2336576</li>
              <li><b>Kerala IT Mission (KSITM):</b> +91 471-2525444 ext 4046/4050, 2335523</li>
              <li><b>Information & Public Relations Dept (PRD):</b> +91 471-2327782, 2518443 (Director) | +91 471-2322475, 2518880 (Secretary)</li>
            </ul>
            <hr />
            <h3>Statewide Helpline Services</h3>
            <table className="emergency-table">
              <thead>
                <tr><th>Service</th><th>Contact Number</th></tr>
              </thead>
              <tbody>
                <tr><td>National Emergency (Police, Fire, Ambulance)</td><td>112</td></tr>
                <tr><td>Police (non-emergency)</td><td>100</td></tr>
                <tr><td>Fire Department</td><td>101</td></tr>
                <tr><td>Ambulance (local)</td><td>102</td></tr>
                <tr><td>Disaster Management Control Room</td><td>108</td></tr>
                <tr><td>State Disaster Helpline</td><td>1077</td></tr>
                <tr><td>Cyber Crime Helpline</td><td>1930</td></tr>
                <tr><td>Crime Stopper Hotline</td><td>1090</td></tr>
                <tr><td>Railway Police Alert</td><td>9846200100</td></tr>
                <tr><td>Highway Alert</td><td>9846100100</td></tr>
                <tr><td>Pink Police Helpline (Thiruvananthapuram city)</td><td>1515</td></tr>
                <tr><td>Women’s Helpline (SNEHITHA)</td><td>1091, 181</td></tr>
                <tr><td>Child Helpline (CHILDLINE)</td><td>1098</td></tr>
                <tr><td>Senior Citizens Helpline (Elderline)</td><td>14567</td></tr>
                <tr><td>AIDS Helpline</td><td>1097</td></tr>
                <tr><td>Tele-MANAS (National Mental Health Line)</td><td>14416</td></tr>
                <tr><td>Kerala State Consumer Affairs Helpline</td><td>1800-425-1550</td></tr>
                <tr><td>Legal Aid Helpline (KSLSA)</td><td>1516</td></tr>
                <tr><td>Anti-Corruption Bureau (VACB)</td><td>1064, WhatsApp 9447789100</td></tr>
                <tr><td>State Health Helpline (24x7)</td><td>104</td></tr>
                <tr><td>COVID-19 DISHA Helpline</td><td>1056, 0471-2552056</td></tr>
              </tbody>
            </table>
            <hr />
            <h3>District & Department Contacts</h3>
            <ul>
              <li><b>District Control Room / Collectorate (Thiruvananthapuram):</b> 0471-2730067</li>
              <li><b>District Media Cell (Thiruvananthapuram):</b> 0471-2730087</li>
              <li><b>Disaster Management Services (Thiruvananthapuram):</b> 0471-2730045</li>
              <li><b>SMS Centre (Thiruvananthapuram):</b> 9497900000</li>
              <li><b>Tourist Alert (Thiruvananthapuram):</b> 9846300100</li>
              <li><b>LSGD Panchayat Office Contacts:</b> Thiruvananthapuram: 0471-2733593, Kollam: 0474-2793431, Alappuzha: 0477-2252784, Ernakulam: 0484-2422216, Idukki: 04862-222815</li>
              <li><b>Kerala Tourism Department State HQ (Trivandrum):</b> 0471-2321132</li>
              <li><b>Kerala Tourism Toll-free (within India):</b> 1800-425-4747</li>
              <li><b>Kerala Tourism Regional Offices:</b> Kollam: 0474-2761555, Idukki: 04869-222620, Ernakulam: 0484-2360502, Kozhikode: 0495-2373862</li>
            </ul>
            <hr />
            <p style={{fontSize: '1rem', marginTop: 24}}><b>Need Something More?</b> If you want district-specific control rooms, departmental nodal officers, or office contacts for specific services (e.g. agriculture, electricity, transport), just let us know!</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;