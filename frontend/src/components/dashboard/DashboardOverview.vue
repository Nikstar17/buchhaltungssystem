<template>
  <div class="flex min-h-screen">
    <main class="flex-1 p-6">
      <!-- Content Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Einnahmen/Ausgaben -->
        <div class="bg-white rounded-xl shadow p-4">
          <h3 class="font-semibold mb-2">Monat März</h3>
          <p>📈 Einnahmen: <strong>1.200 €</strong></p>
          <p>📉 Ausgaben: <strong>980 €</strong></p>
        </div>

        <!-- Letzte Buchungen -->
        <div class="bg-white rounded-xl shadow p-4">
          <h3 class="font-semibold mb-2">Letzte Buchungen</h3>
          <ul class="list-disc list-inside space-y-1">
            <li>[01.03] Tanken – Auto – 45,00 €</li>
            <li>[02.03] Rechnung Kunde – Einnahme – 300,00 €</li>
          </ul>
        </div>

        <!-- Hochgeladene Belege -->
        <div class="bg-white rounded-xl shadow p-4">
          <h3 class="font-semibold mb-2">Neueste Belege</h3>
          <ul class="list-disc list-inside space-y-1">
            <li>[PDF] 02.03.2025 – Rechnung A</li>
            <li>[PDF] 01.03.2025 – Kassenbon Supermarkt</li>
          </ul>
        </div>

        <!-- Diagramm (Platzhalter) -->
        <div class="bg-white rounded-xl shadow p-4">
          <h3 class="font-semibold mb-2">Diagramm Einnahmen/Ausgaben</h3>
          <div class="h-40 flex items-center justify-center text-gray-400">[📈 Diagramm folgt]</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup></script>

<style scoped></style>
