import xml.etree.ElementTree as ET
import json

# XML-Daten als String
xml_data = '''<?xml version="1.0" encoding="utf-8"?>
<gnc-account-example
  xmlns="http://www.gnucash.org/XML/"
  xmlns:act="http://www.gnucash.org/XML/act"
  xmlns:addr="http://www.gnucash.org/XML/addr"
  xmlns:bgt="http://www.gnucash.org/XML/bgt"
  xmlns:billterm="http://www.gnucash.org/XML/billterm"
  xmlns:book="http://www.gnucash.org/XML/book"
  xmlns:bt-days="http://www.gnucash.org/XML/bt-days"
  xmlns:bt-prox="http://www.gnucash.org/XML/bt-prox"
  xmlns:cd="http://www.gnucash.org/XML/cd"
  xmlns:cmdty="http://www.gnucash.org/XML/cmdty"
  xmlns:cust="http://www.gnucash.org/XML/cust"
  xmlns:employee="http://www.gnucash.org/XML/employee"
  xmlns:fs="http://www.gnucash.org/XML/fs"
  xmlns:gnc="http://www.gnucash.org/XML/gnc"
  xmlns:gnc-act="http://www.gnucash.org/XML/gnc-act"
  xmlns:invoice="http://www.gnucash.org/XML/invoice"
  xmlns:job="http://www.gnucash.org/XML/job"
  xmlns:lot="http://www.gnucash.org/XML/lot"
  xmlns:order="http://www.gnucash.org/XML/order"
  xmlns:owner="http://www.gnucash.org/XML/owner"
  xmlns:price="http://www.gnucash.org/XML/price"
  xmlns:recurrence="http://www.gnucash.org/XML/recurrence"
  xmlns:slot="http://www.gnucash.org/XML/slot"
  xmlns:split="http://www.gnucash.org/XML/split"
  xmlns:sx="http://www.gnucash.org/XML/sx"
  xmlns:taxtable="http://www.gnucash.org/XML/taxtable"
  xmlns:trn="http://www.gnucash.org/XML/trn"
  xmlns:ts="http://www.gnucash.org/XML/ts"
  xmlns:tte="http://www.gnucash.org/XML/tte"
  xmlns:entry="http://www.gnucash.org/XML/entry"
  xmlns:vendor="http://www.gnucash.org/XML/vendor">

  <gnc-act:title>
    Kontenrahmen SKR03
  </gnc-act:title>
  <gnc-act:short-description>
    Standardkontenrahmen SKR03
  </gnc-act:short-description>
  <gnc-act:long-description>
    Beta Version des Kontenrahmes SKR03 zum Erweitern und Umstrukturieren. Der Kontenrahmen sollte den eigenen Bedürfnissen angepasst werden was Struktur und Kontenbezeichnungen angeht. WICHTIG!: Die Privatkonten fließen nicht in die Berechnung des Berichtes Bilanz, sind jedoch im Bericht Bilanz aufgeführt. Die im Bericht Bilanz aufgeführte Passiva "Gewinnrücklagen" gibt den Saldo der GuV aus. Die Anlage dieses Kontenrahmens wurde von der Firma LiHAS - Linuxhaus Stuttgart - unterstützt.
  </gnc-act:long-description>
  <gnc-act:exclude-from-select-all>1</gnc-act:exclude-from-select-all>

  <gnc:account version="2.0.0">
    <act:name>Root Account</act:name>
    <act:id type="new">1972cce2e2364f95b2b0bc014502661d</act:id>
    <act:type>ROOT</act:type>
    <act:commodity-scu>0</act:commodity-scu>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Aktiva</act:name>
    <act:id type="new">fc3b1f110a6686f3d40bb0c41c0f8de0</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:description>Aktiva</act:description>
    <act:parent type="new">1972cce2e2364f95b2b0bc014502661d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Anlage- u. Kapitalkonten 0</act:name>
    <act:id type="new">27356188a1963c1dbf943022441d095f</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
      <slot>
	<slot:key>tax-related</slot:key>
	<slot:value type="integer">1</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">fc3b1f110a6686f3d40bb0c41c0f8de0</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>0027 EDV-Software</act:name>
    <act:id type="new">8275e7a0b489940a2ba993f9019a898f</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>0027</act:code>
    <act:slots>
      <slot>
	<slot:key>tax-related</slot:key>
	<slot:value type="integer">1</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">27356188a1963c1dbf943022441d095f</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>0410 Geschäftsausstattung</act:name>
    <act:id type="new">a588283077bd935dede66d13b2ee478f</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>0410</act:code>
    <act:slots>
      <slot>
	<slot:key>tax-related</slot:key>
	<slot:value type="integer">1</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">27356188a1963c1dbf943022441d095f</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>0420 Büroeinrichtung</act:name>
    <act:id type="new">573063d23b81fe3f9917d80fe6cc41e7</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>0420</act:code>
    <act:slots>
      <slot>
	<slot:key>tax-related</slot:key>
	<slot:value type="integer">1</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">27356188a1963c1dbf943022441d095f</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>0565 Darlehen</act:name>
    <act:id type="new">bd74fcb2d15fc7540ecc5ba8f27cbf48</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>0565</act:code>
    <act:parent type="new">27356188a1963c1dbf943022441d095f</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>0210 Maschinen</act:name>
    <act:id type="new">904b262e6f84659046267cad87ac5e90</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>0210</act:code>
    <act:parent type="new">27356188a1963c1dbf943022441d095f</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>0400 Betriebsausstattung</act:name>
    <act:id type="new">910d6c057660045a9958fb5a57ffc899</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>0400</act:code>
    <act:parent type="new">27356188a1963c1dbf943022441d095f</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>0430 Ladeneinrichtung</act:name>
    <act:id type="new">2876b41c069107076e7a18ec39bf4f9c</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>0430</act:code>
    <act:parent type="new">27356188a1963c1dbf943022441d095f</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Finanzkonten 1</act:name>
    <act:id type="new">1b13a7614b5e84b0778963995e20d897</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">fc3b1f110a6686f3d40bb0c41c0f8de0</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1100 Postbank</act:name>
    <act:id type="new">9fe8d61dac9cf62b3f12e6c71a4385b2</act:id>
    <act:type>BANK</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1100</act:code>
    <act:parent type="new">1b13a7614b5e84b0778963995e20d897</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1200 Bankkonto</act:name>
    <act:id type="new">875ec51cd332f3b75c15a2a9ca309ebd</act:id>
    <act:type>BANK</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1200</act:code>
    <act:parent type="new">1b13a7614b5e84b0778963995e20d897</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1590 Durchlaufende Posten</act:name>
    <act:id type="new">f048cb49a135a298d5df958a4c63ba22</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1590</act:code>
    <act:parent type="new">1b13a7614b5e84b0778963995e20d897</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1371 Gewinnermittlung §4/3 nicht Ergebniswirksam</act:name>
    <act:id type="new">58c8b84a785d7feac255d381943076df</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1371</act:code>
    <act:parent type="new">1b13a7614b5e84b0778963995e20d897</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1571 Abziehbare VSt. 7%</act:name>
    <act:id type="new">7edc3c319713c53035b3e439ccec5e2b</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1571</act:code>
    <act:parent type="new">1b13a7614b5e84b0778963995e20d897</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1576 Abziehbare VSt. 19%</act:name>
    <act:id type="new">507b25d5d47d57ba115929b70a32fa5e</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1576</act:code>
    <act:parent type="new">1b13a7614b5e84b0778963995e20d897</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1577 Abziehbare VStr. nach §13b UStG 19%</act:name>
    <act:id type="new">ac0fb64d0cfc2b88444527ce8c8682fe</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1577</act:code>
    <act:parent type="new">1b13a7614b5e84b0778963995e20d897</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1400 Ford. a. Lieferungen und Leistungen</act:name>
    <act:id type="new">2fe36b4ddde053387e42aa893a94b91b</act:id>
    <act:type>RECEIVABLE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1400</act:code>
    <act:parent type="new">1b13a7614b5e84b0778963995e20d897</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Wareneingangs- u. Bestandskonten 3</act:name>
    <act:id type="new">a26df9927a82bcb58a1facb4cde6f221</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">fc3b1f110a6686f3d40bb0c41c0f8de0</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>3120 Leistungen §13b UStG 19% Vorsteuer, 19% Umsatzsteuer</act:name>
    <act:id type="new">39c180a4e3647d347ebc3e16e984372b</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>3120</act:code>
    <act:parent type="new">a26df9927a82bcb58a1facb4cde6f221</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>3400 Wareneingang VSt. 19%</act:name>
    <act:id type="new">01e4b246665a54d40466ba88f5d1d34e</act:id>
    <act:type>ASSET</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>3400</act:code>
    <act:slots>
      <slot>
	<slot:key>tax-related</slot:key>
	<slot:value type="integer">1</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">a26df9927a82bcb58a1facb4cde6f221</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Passiva</act:name>
    <act:id type="new">845b29bc14787bded30488e8d51eec0b</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:description>Passiva</act:description>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">1972cce2e2364f95b2b0bc014502661d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Umsatzsteuer</act:name>
    <act:id type="new">dea7f32e6a447d2d1cd7048932c98265</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">845b29bc14787bded30488e8d51eec0b</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1771 Umsatzsteuer 7%</act:name>
    <act:id type="new">d699c440f7817339d2fe60dd875520b6</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1771</act:code>
    <act:parent type="new">dea7f32e6a447d2d1cd7048932c98265</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1776 Umsatzsteuer 19%</act:name>
    <act:id type="new">55a2876edef147ed7631486de4af558c</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1776</act:code>
    <act:parent type="new">dea7f32e6a447d2d1cd7048932c98265</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1780 Umsatzsteuer-Vorauszahlung</act:name>
    <act:id type="new">4b5e1c2b17024a7721d0955c9f140dd6</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1780</act:code>
    <act:parent type="new">dea7f32e6a447d2d1cd7048932c98265</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1781 Umsatzsteuer-Vorauszahlung 1/11</act:name>
    <act:id type="new">08793cd11dfca23d7b435a7338db02da</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1781</act:code>
    <act:parent type="new">dea7f32e6a447d2d1cd7048932c98265</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1787 Umsatzsteuer § 13b UStG 19%</act:name>
    <act:id type="new">8e1583dfe60365b756f5365741250001</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1787</act:code>
    <act:parent type="new">dea7f32e6a447d2d1cd7048932c98265</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1790 Umsatzsteuer Vorjahr</act:name>
    <act:id type="new">635fe36261db8b9beda522420f564028</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1790</act:code>
    <act:parent type="new">dea7f32e6a447d2d1cd7048932c98265</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1791 Umsatzsteuer frühere Jahre</act:name>
    <act:id type="new">b2d79b416fee27d4d6a38643f6ad0d45</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1791</act:code>
    <act:parent type="new">dea7f32e6a447d2d1cd7048932c98265</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Verbindlichkeiten</act:name>
    <act:id type="new">a31fca8b7c5eb2cb0111f1f97696ac93</act:id>
    <act:type>LIABILITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">845b29bc14787bded30488e8d51eec0b</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1600 Verblk. aus Lieferungen u. Leistungen</act:name>
    <act:id type="new">1bf9f2675a36b278adcf6da68a7e4cbe</act:id>
    <act:type>PAYABLE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1600</act:code>
    <act:parent type="new">a31fca8b7c5eb2cb0111f1f97696ac93</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Erlöse u. Erträge 2/8</act:name>
    <act:id type="new">3f31fc649f19b5201f22f7648c3f7107</act:id>
    <act:type>INCOME</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">1972cce2e2364f95b2b0bc014502661d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Erlöskonten 8</act:name>
    <act:id type="new">fd04e181ab83b37b80a4609b0806e954</act:id>
    <act:type>INCOME</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">3f31fc649f19b5201f22f7648c3f7107</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>8400 Erlöse USt. 19%</act:name>
    <act:id type="new">d75d796e879b0ad9b2732d698ae9e838</act:id>
    <act:type>INCOME</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>8400</act:code>
    <act:slots>
      <slot>
	<slot:key>tax-related</slot:key>
	<slot:value type="integer">1</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">fd04e181ab83b37b80a4609b0806e954</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>8300 Erlöse USt. 7%</act:name>
    <act:id type="new">0c82316c2aecaa02ce1b4ecb223f6f5d</act:id>
    <act:type>INCOME</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>8300</act:code>
    <act:parent type="new">fd04e181ab83b37b80a4609b0806e954</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Ertragskonten 2</act:name>
    <act:id type="new">4f552b822559c82eaa816d0049f70064</act:id>
    <act:type>INCOME</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">3f31fc649f19b5201f22f7648c3f7107</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>2650 sonstige Zinsen und ähnliche Erträge</act:name>
    <act:id type="new">cc08ab7c747853f5f7ea6b384fdd8b4d</act:id>
    <act:type>INCOME</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>2650</act:code>
    <act:parent type="new">4f552b822559c82eaa816d0049f70064</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>2500 Außerordentliche Erträge</act:name>
    <act:id type="new">5634359999c43ba58697553d1d905c4c</act:id>
    <act:type>INCOME</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>2500</act:code>
    <act:parent type="new">4f552b822559c82eaa816d0049f70064</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>2700 Sonstige Erträge</act:name>
    <act:id type="new">067716095fef7e694a2e0c40f1eaaefd</act:id>
    <act:type>INCOME</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>2700</act:code>
    <act:parent type="new">4f552b822559c82eaa816d0049f70064</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Aufwendungen 2/4</act:name>
    <act:id type="new">be324e400d3b67510f89afd18de776e3</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">1972cce2e2364f95b2b0bc014502661d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Abschreibungen</act:name>
    <act:id type="new">ad3f063a8200c1faa0331e2d9eb3ae04</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">be324e400d3b67510f89afd18de776e3</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4855 Sofortabschreibung GWG</act:name>
    <act:id type="new">cf214c888424ce036704bd526650a4c1</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4855</act:code>
    <act:parent type="new">ad3f063a8200c1faa0331e2d9eb3ae04</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Kfz-Kosten</act:name>
    <act:id type="new">8488954a5834d5484ed57439a0d43305</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">be324e400d3b67510f89afd18de776e3</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4510 Kfz-Steuer</act:name>
    <act:id type="new">4355e4bceaa024b71efb3223ac6576c0</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4510</act:code>
    <act:parent type="new">8488954a5834d5484ed57439a0d43305</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4520 Kfz-Versicherungen</act:name>
    <act:id type="new">4395e7b49fc7d34db620e6249836d747</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4520</act:code>
    <act:parent type="new">8488954a5834d5484ed57439a0d43305</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4530 laufende Kfz-Betriebskosten</act:name>
    <act:id type="new">9bcbd663916f135d81b8eff6dc8b8819</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4530</act:code>
    <act:parent type="new">8488954a5834d5484ed57439a0d43305</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4540 Kfz-Reparaturen</act:name>
    <act:id type="new">5359164e661dd33c4bdb98b5149b07d1</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4540</act:code>
    <act:parent type="new">8488954a5834d5484ed57439a0d43305</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4570 Fremdfahrzeuge</act:name>
    <act:id type="new">3b92417001893aa765edaa7109b2d48a</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4570</act:code>
    <act:parent type="new">8488954a5834d5484ed57439a0d43305</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4580 sonstige Kfz-Kosten</act:name>
    <act:id type="new">e4c3ff3a921558869191a648aeb9b0e3</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4580</act:code>
    <act:parent type="new">8488954a5834d5484ed57439a0d43305</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Personalkosten</act:name>
    <act:id type="new">43953979cf408743814cb6887d5ec022</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">be324e400d3b67510f89afd18de776e3</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4120 Gehälter</act:name>
    <act:id type="new">8f21199517fcfd70ad2ad6aaa3e714b6</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4120</act:code>
    <act:parent type="new">43953979cf408743814cb6887d5ec022</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4130 gesetzliche soziale Aufwendungen</act:name>
    <act:id type="new">46ba645d075b6a1f3a38824d812f8818</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4130</act:code>
    <act:parent type="new">43953979cf408743814cb6887d5ec022</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4165 Aufwendungen für Altersvorsorge</act:name>
    <act:id type="new">e89eafba1acc736a7ba74882a7f8c836</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4165</act:code>
    <act:parent type="new">43953979cf408743814cb6887d5ec022</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4170 Vermögenswirksame Leistungen</act:name>
    <act:id type="new">88bc69e1ff8977cd70c52567dde8107d</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4170</act:code>
    <act:parent type="new">43953979cf408743814cb6887d5ec022</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4190 Aushilfslöhne</act:name>
    <act:id type="new">d74350b9ad5583b533fd906ec837d9fe</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4190</act:code>
    <act:parent type="new">43953979cf408743814cb6887d5ec022</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Raumkosten</act:name>
    <act:id type="new">9adef6f318a931fbb8519a823e2c20e8</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">be324e400d3b67510f89afd18de776e3</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4210 Miete und Nebenkosten</act:name>
    <act:id type="new">b6e84a2fcf1754f1f6f1f71913f03a1d</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4210</act:code>
    <act:parent type="new">9adef6f318a931fbb8519a823e2c20e8</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4240 Gas, Wasser, Strom (Verwaltung, Vertrieb)</act:name>
    <act:id type="new">d41823e7c279286dd74c6ec757dcb305</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4240</act:code>
    <act:parent type="new">9adef6f318a931fbb8519a823e2c20e8</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4250 Reinigung</act:name>
    <act:id type="new">db313359a146b610ce80a36dde18bf01</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4250</act:code>
    <act:parent type="new">9adef6f318a931fbb8519a823e2c20e8</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Reparatur/Instandhaltung</act:name>
    <act:id type="new">accaec28a4afcf3c82570da4c9343c2d</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">be324e400d3b67510f89afd18de776e3</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4805 Reparatur u. Instandh. von Anlagen/Maschinen u. Betriebs- u. Geschäftsausst.</act:name>
    <act:id type="new">b5d6461bb3028d13faa8bee2981925a1</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4805</act:code>
    <act:parent type="new">accaec28a4afcf3c82570da4c9343c2d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Versicherungsbeiträge</act:name>
    <act:id type="new">709bf14d69164a6c2a48e6c0e13ece37</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">be324e400d3b67510f89afd18de776e3</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4360 Versicherungen</act:name>
    <act:id type="new">7484251f3d5fc7ec71419b2fba733a78</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4360</act:code>
    <act:parent type="new">709bf14d69164a6c2a48e6c0e13ece37</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4380 Beiträge</act:name>
    <act:id type="new">f2b1ad75fd3b7fc4473972a9c2675cbf</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4380</act:code>
    <act:parent type="new">709bf14d69164a6c2a48e6c0e13ece37</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4390 sonstige Ausgaben</act:name>
    <act:id type="new">a2d552e480b95123e90be434b3ac9653</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4390</act:code>
    <act:parent type="new">709bf14d69164a6c2a48e6c0e13ece37</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4396 steuerlich abzugsfähige Verspätungszuschläge und Zwangsgelder</act:name>
    <act:id type="new">0c73c5dc5e72bb4962b83ddc85991101</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4396</act:code>
    <act:parent type="new">709bf14d69164a6c2a48e6c0e13ece37</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Werbe-/Reisekosten</act:name>
    <act:id type="new">a657ade965a1429d44d830d3832bf9aa</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">be324e400d3b67510f89afd18de776e3</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4610 Werbekosten</act:name>
    <act:id type="new">2d90f835fcb74d7a77b4a2a2b40c777a</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4610</act:code>
    <act:parent type="new">a657ade965a1429d44d830d3832bf9aa</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4653 Aufmerksamkeiten</act:name>
    <act:id type="new">790770c5f93cff7d585bca1627446716</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4653</act:code>
    <act:parent type="new">a657ade965a1429d44d830d3832bf9aa</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4665 nicht abzugsfähige Betriebsausg. aus Werbe-, Repräs.- u. Reisekosten</act:name>
    <act:id type="new">235a6225c2c7d2ffa865345e78cae283</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4665</act:code>
    <act:parent type="new">a657ade965a1429d44d830d3832bf9aa</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4670 Reisekosten Unternehmer</act:name>
    <act:id type="new">dda3ae53573975cd05fab1d3cdf40806</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4670</act:code>
    <act:parent type="new">a657ade965a1429d44d830d3832bf9aa</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>verschiedene Kosten</act:name>
    <act:id type="new">d0c00095e4b00f9f25253307be05e885</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">be324e400d3b67510f89afd18de776e3</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4910 Porto</act:name>
    <act:id type="new">b84666b6b2d17f4be4a2cc15e595b30d</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4910</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4920 Telekom</act:name>
    <act:id type="new">892bb0974aa6c422f63b5df5354e8f7f</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4920</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4921 Mobilfunk D2</act:name>
    <act:id type="new">20a13b07d90c5b385e78190525439aa2</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4921</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4922 Internet</act:name>
    <act:id type="new">4d57d9103ab150ad4f01bc7a918fd0cc</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4922</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4930 Bürobedarf</act:name>
    <act:id type="new">ac4d7c452835096c373f1a94dc3104f4</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4930</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4940 Zeitschriften, Bücher</act:name>
    <act:id type="new">1bac306450e7bc0619e42c11ab791204</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4940</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4945 Fortbildungskosten</act:name>
    <act:id type="new">6be35acc206b144ee23c07086bc7a856</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4945</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4955 Buchführungskosten</act:name>
    <act:id type="new">25afa584627e0c0e8681bd8a82a77d14</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4955</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4957 Abschluß- u. Prüfungskosten</act:name>
    <act:id type="new">bf093094a55c036a193357ebcafcab67</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4957</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4970 Nebenkosten des Geldverkehrs</act:name>
    <act:id type="new">4f476c9b65684d56630db45690b9d4fc</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4970</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>4985 Werkzeuge und Kleingeräte</act:name>
    <act:id type="new">a5b36148c3fc06080973a5d25f28225b</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>4985</act:code>
    <act:parent type="new">d0c00095e4b00f9f25253307be05e885</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Zinsaufwendungen</act:name>
    <act:id type="new">8d2641f8bbc41aa863274bb496002f3e</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">be324e400d3b67510f89afd18de776e3</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>2110 Zinsaufwendungen für kurzfristige Verbindlichkeiten</act:name>
    <act:id type="new">2d20e36f8abb4e366c8e3e2783bdafab</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>2110</act:code>
    <act:parent type="new">8d2641f8bbc41aa863274bb496002f3e</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>2121 Zinsaufwendungen für KFZ Finanzierung</act:name>
    <act:id type="new">17651501792b93b06832634462ddddae</act:id>
    <act:type>EXPENSE</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>2121</act:code>
    <act:parent type="new">8d2641f8bbc41aa863274bb496002f3e</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Anfangsbestand 9</act:name>
    <act:id type="new">2d4eb2e0ef3bab0ac50b87c84babcf5d</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:description>Saldenvortragskonten</act:description>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">1972cce2e2364f95b2b0bc014502661d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Saldenvortragskonten</act:name>
    <act:id type="new">26c3f10c1c7621661c1b813d6141280d</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">2d4eb2e0ef3bab0ac50b87c84babcf5d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>9000 Saldenvortrag Sachkonten</act:name>
    <act:id type="new">fa346eee1add66248bff420aafeebebb</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>9000</act:code>
    <act:parent type="new">26c3f10c1c7621661c1b813d6141280d</act:parent>
  <act:slots>
    <slot>
      <slot:key>equity-type</slot:key>
      <slot:value type="string">opening-balance</slot:value>
    </slot>
  </act:slots>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>9008 Saldenvorträge Debitoren</act:name>
    <act:id type="new">1f36ecbf065faa2b25a0749ceee72efa</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>9008</act:code>
    <act:parent type="new">26c3f10c1c7621661c1b813d6141280d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>9009 Saldenvorträge Kreditoren</act:name>
    <act:id type="new">a6c754f12d0b9129790d9f52c5361778</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>9009</act:code>
    <act:parent type="new">26c3f10c1c7621661c1b813d6141280d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Privatkonten 1</act:name>
    <act:id type="new">1888a7d2fbbdede8446090a31651565f</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">1972cce2e2364f95b2b0bc014502661d</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>Privatentnahmen/-einlagen</act:name>
    <act:id type="new">b9ae1b059749ea81c757a9adad39db1b</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:slots>
      <slot>
	<slot:key>placeholder</slot:key>
	<slot:value type="string">true</slot:value>
      </slot>
    </act:slots>
    <act:parent type="new">1888a7d2fbbdede8446090a31651565f</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1800 Privatentnahme allgemein</act:name>
    <act:id type="new">0e6b8f9c973149c8d1c00e40919e9e21</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1800</act:code>
    <act:parent type="new">b9ae1b059749ea81c757a9adad39db1b</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1810 Privatsteuern</act:name>
    <act:id type="new">fff2b92b43dc9d9690a7e5c365d2baf6</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1810</act:code>
    <act:parent type="new">b9ae1b059749ea81c757a9adad39db1b</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1820 Sonderausgaben beschränkt abzugsfähig</act:name>
    <act:id type="new">5c008564ba99d0dfe6f20166adde5e6c</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1820</act:code>
    <act:parent type="new">b9ae1b059749ea81c757a9adad39db1b</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1830 Sonderausgaben unbeschränkt abzugsfähig</act:name>
    <act:id type="new">d89a53718b4753ac5407b38ab43f1339</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1830</act:code>
    <act:parent type="new">b9ae1b059749ea81c757a9adad39db1b</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1850 Außergewöhnliche Belastungen</act:name>
    <act:id type="new">ab2c3c1b68e9c21ca3bce32c729c5cdc</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1850</act:code>
    <act:parent type="new">b9ae1b059749ea81c757a9adad39db1b</act:parent>
  </gnc:account>
  <gnc:account version="2.0.0">
    <act:name>1890 Privateinlagen</act:name>
    <act:id type="new">4057a69542c170211849f7705354aadb</act:id>
    <act:type>EQUITY</act:type>
    <act:commodity>
      <cmdty:space>ISO4217</cmdty:space>
      <cmdty:id>EUR</cmdty:id>
    </act:commodity>
    <act:commodity-scu>100</act:commodity-scu>
    <act:code>1890</act:code>
    <act:parent type="new">b9ae1b059749ea81c757a9adad39db1b</act:parent>
  </gnc:account>

</gnc-account-example>'''

# XML parsen
tree = ET.ElementTree(ET.fromstring(xml_data))
root = tree.getroot()

# Namespace-Management
namespaces = {
    '': 'http://www.gnucash.org/XML/',  # Default Namespace
    'act': 'http://www.gnucash.org/XML/act',
    'cmdty': 'http://www.gnucash.org/XML/cmdty',
    'gnc': 'http://www.gnucash.org/XML/gnc',
    'slot': 'http://www.gnucash.org/XML/slot',
    'gnc-act': 'http://www.gnucash.org/XML/gnc-act'
}

# Funktion zum Parsen eines Accounts
def parse_account(account_elem):
    account = {}
    account['name'] = account_elem.find('act:name', namespaces).text
    account['id'] = account_elem.find('act:id', namespaces).text
    account['type'] = account_elem.find('act:type', namespaces).text

    commodity_elem = account_elem.find('act:commodity', namespaces)
    if commodity_elem is not None:
        account['commodity'] = {
            'space': commodity_elem.find('cmdty:space', namespaces).text,
            'id': commodity_elem.find('cmdty:id', namespaces).text
        }

    account['commodity_scu'] = account_elem.find('act:commodity-scu', namespaces).text

    description_elem = account_elem.find('act:description', namespaces)
    if description_elem is not None:
        account['description'] = description_elem.text

    code_elem = account_elem.find('act:code', namespaces)
    if code_elem is not None:
        account['code'] = code_elem.text

    parent_elem = account_elem.find('act:parent', namespaces)
    if parent_elem is not None:
        account['parent_id'] = parent_elem.text

    slots_elem = account_elem.find('act:slots', namespaces)
    if slots_elem is not None:
        account['slots'] = []
        for slot in slots_elem.findall('slot', namespaces):
            slot_key = slot.find('slot:key', namespaces).text
            slot_value = slot.find('slot:value', namespaces).text
            account['slots'].append({'key': slot_key, 'value': slot_value})

    return account

# Extrahieren der Konten
accounts = []
for account_elem in root.findall('gnc:account', namespaces):
    accounts.append(parse_account(account_elem))

# Erstellen der JSON-Ausgabe
output = {
    'title': root.find('gnc-act:title', namespaces).text,
    'short_description': root.find('gnc-act:short-description', namespaces).text,
    'long_description': root.find('gnc-act:long-description', namespaces).text,
    'accounts': accounts
}

# JSON ausgeben
json_output = json.dumps(output, indent=4, ensure_ascii=False)

# JSON in Datei speichern
with open('skr04.json', 'w', encoding='utf-8') as json_file:
  json_file.write(json_output)