<template>
  <div class="min-h-screen p-6">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">Kontenrahmen-Einstellungen</h1>

    <div v-if="loading" class="flex justify-center items-center py-10">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
    </div>

    <div v-else class="grid grid-cols-1 gap-6">
      <!-- Kontenrahmen Auswahl Karte -->
      <div class="bg-white rounded-xl shadow-md overflow-hidden p-6">
        <h2 class="text-lg font-semibold mb-4 text-gray-800 border-b pb-2">Kontenrahmen auswählen</h2>

        <div class="mb-6">
          <label for="chart-of-accounts" class="block text-sm font-semibold text-gray-700 mb-2">
            Verfügbare Kontenrahmen
          </label>

          <div class="relative">
            <select id="chart-of-accounts" v-model="selectedChartId" @change="handleChartChange"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200 appearance-none bg-white">
              <option value="" disabled>Bitte wählen Sie einen Kontenrahmen</option>
              <option v-for="chart in chartOfAccounts" :key="chart.id" :value="chart.id">
                {{ chart.name }} {{ isActiveChart(chart.id) ? '(Aktiv)' : '' }}
              </option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </div>
          </div>
        </div>

        <div v-if="selectedChart" class="border-t pt-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 class="text-sm uppercase tracking-wide text-gray-500 font-medium mb-1">Name</h3>
              <p class="text-gray-800">{{ selectedChart.name }}</p>
            </div>

            <div>
              <h3 class="text-sm uppercase tracking-wide text-gray-500 font-medium mb-1">Status</h3>
              <p class="text-gray-800">
                <span v-if="isActiveChart(selectedChart.id)" class="text-green-600 font-medium">
                  Aktiv
                </span>
                <span v-else class="text-gray-500">
                  Inaktiv
                </span>
              </p>
            </div>
          </div>

          <div class="mt-4">
            <h3 class="text-sm uppercase tracking-wide text-gray-500 font-medium mb-1">Beschreibung</h3>
            <p class="text-gray-800">{{ selectedChart.description || 'Keine Beschreibung vorhanden' }}</p>
          </div>

          <div class="mt-6 flex justify-end">
            <button @click="activateChart" :disabled="isActiveChart(selectedChart.id) || activating" :class="[
              'px-4 py-2 rounded-lg transition-colors duration-200',
              isActiveChart(selectedChart.id)
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            ]">
              <span v-if="activating" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                  </path>
                </svg>
                Wird aktiviert...
              </span>
              <span v-else-if="isActiveChart(selectedChart.id)">
                Bereits aktiv
              </span>
              <span v-else>
                Aktivieren
              </span>
            </button>
          </div>
        </div>
      </div>

      <!-- Konten Tabelle -->
      <div v-if="selectedChart" class="bg-white rounded-xl shadow-md overflow-hidden p-6">
        <h2 class="text-lg font-semibold mb-4 text-gray-800 border-b pb-2">Konten im Kontenrahmen</h2>

        <div v-if="loadingAccounts" class="flex justify-center items-center py-10">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
        </div>

        <div v-else>
          <!-- Suchfilter -->
          <div class="mb-4 relative">
            <input type="text" v-model="searchQuery" placeholder="Konten durchsuchen..."
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <span class="absolute inset-y-0 right-0 flex items-center pr-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                  clip-rule="evenodd" />
              </svg>
            </span>
          </div>

          <!-- Kontrollknöpfe zum Ein-/Ausklappen -->
          <div class="mb-4 flex flex-wrap gap-2">
            <button @click="toggleAllClasses"
              class="text-xs bg-blue-100 hover:bg-blue-200 text-blue-700 font-medium py-1 px-2 rounded transition-colors duration-200 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path v-if="areAllClassesCollapsed" d="M5 8l5 5 5-5H5z" />
                <path v-else d="M5 12l5-5 5 5H5z" />
              </svg>
              {{ areAllClassesCollapsed ? 'Alle Klassen ausklappen' : 'Alle Klassen einklappen' }}
            </button>
            <button @click="toggleAllGroups"
              class="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-1 px-2 rounded transition-colors duration-200 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path v-if="areAllGroupsCollapsed" d="M5 8l5 5 5-5H5z" />
                <path v-else d="M5 12l5-5 5 5H5z" />
              </svg>
              {{ areAllGroupsCollapsed ? 'Alle Gruppen ausklappen' : 'Alle Gruppen einklappen' }}
            </button>
          </div>

          <!-- Konten Tabelle -->
          <div>
            <div v-if="accounts.length > 0 && filteredAccounts.length > 0">
              <!-- Gruppierte Tabellen nach Kontenklassen -->
              <div v-for="group in groupedAccounts" :key="group.className" class="mb-8">
                <h3 @click="toggleClassCollapse(group.className)"
                  class="text-md font-bold mb-2 bg-blue-50 text-blue-700 p-3 rounded-lg shadow-sm flex justify-between items-center cursor-pointer hover:bg-blue-100 transition-colors duration-200">
                  <div class="flex items-center">
                    <span class="inline-block mr-2 text-xs bg-blue-200 text-blue-800 rounded py-0.5 px-2">
                      {{ group.classAccountRange }}
                    </span>
                    {{ group.className }}
                  </div>
                  <span>
                    <svg v-if="collapsedClasses[group.className]" xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5 text-blue-600" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd"
                        d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                        clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" viewBox="0 0 20 20"
                      fill="currentColor">
                      <path fill-rule="evenodd"
                        d="M5.293 12.707a1 1 0 010-1.414L8.586 8l-3.293-3.293a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                        clip-rule="evenodd" />
                    </svg>
                  </span>
                </h3>
                <div v-show="!collapsedClasses[group.className]">
                  <div v-for="accountGroup in group.accountGroups" :key="accountGroup.groupKey" class="mb-4">
                    <h4 @click="toggleGroupCollapse(accountGroup.groupKey)"
                      class="text-sm font-semibold ml-4 mb-2 bg-gray-50 p-2 rounded-lg flex justify-between items-center cursor-pointer hover:bg-gray-100 transition-colors duration-200">
                      <div class="flex items-center">
                        <span
                          class="inline-block mr-2 text-xs bg-gray-200 text-gray-700 rounded py-0.5 px-2 w-20 text-center">
                          {{ accountGroup.accountRange }}
                        </span>
                        {{ accountGroup.groupName }}
                      </div>
                      <span>
                        <svg v-if="collapsedGroups[accountGroup.groupKey]" xmlns="http://www.w3.org/2000/svg"
                          class="h-4 w-4 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd"
                            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                            clip-rule="evenodd" />
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" viewBox="0 0 20 20"
                          fill="currentColor">
                          <path fill-rule="evenodd"
                            d="M5.293 12.707a1 1 0 010-1.414L8.586 8l-3.293-3.293a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                            clip-rule="evenodd" />
                        </svg>
                      </span>
                    </h4>
                    <table v-show="!collapsedGroups[accountGroup.groupKey]"
                      class="min-w-full divide-y divide-gray-200 rounded-lg overflow-hidden shadow-sm ml-6">
                      <thead class="bg-gray-100">
                        <tr>
                          <th scope="col"
                            class="px-4 py-2 text-left text-xs font-medium text-gray-600 uppercase tracking-wider w-24">
                            Konto-Nr.
                          </th>
                          <th scope="col"
                            class="px-4 py-2 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">
                            Name
                          </th>
                          <th scope="col"
                            class="px-4 py-2 text-left text-xs font-medium text-gray-600 uppercase tracking-wider w-28">
                            Typ
                          </th>
                          <th scope="col"
                            class="px-4 py-2 text-left text-xs font-medium text-gray-600 uppercase tracking-wider w-24">
                            Status
                          </th>
                        </tr>
                      </thead>
                      <tbody class="bg-white divide-y divide-gray-100">
                        <tr v-for="account in accountGroup.accounts" :key="account.id"
                          class="hover:bg-gray-50 transition-colors duration-150">
                          <td class="px-4 py-2 whitespace-nowrap">
                            <div class="text-sm font-medium text-gray-900">{{ account.number }}</div>
                          </td>
                          <td class="px-4 py-2">
                            <div class="text-sm text-gray-800">{{ account.name }}</div>
                          </td>
                          <td class="px-4 py-2 whitespace-nowrap">
                            <span class="px-2 inline-flex text-xs leading-5 font-medium rounded-full" :class="{
                              'bg-blue-100 text-blue-800': account.type === 'ASSET',
                              'bg-red-100 text-red-800': account.type === 'LIABILITY',
                              'bg-green-100 text-green-800': account.type === 'REVENUE',
                              'bg-yellow-100 text-yellow-800': account.type === 'EXPENSE',
                              'bg-purple-100 text-purple-800': account.type === 'EQUITY'
                            }">
                              {{ getAccountTypeName(account.type) }}
                            </span>
                          </td>
                          <td class="px-4 py-2 whitespace-nowrap">
                            <span class="inline-flex items-center">
                              <span class="h-2.5 w-2.5 rounded-full mr-2"
                                :class="account.active ? 'bg-green-500' : 'bg-gray-400'"></span>
                              <span class="text-xs text-gray-700">{{ account.active ? 'Aktiv' : 'Inaktiv' }}</span>
                            </span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <div v-else>
              <p class="px-6 py-4 text-center text-sm text-gray-500">
                {{ accounts.length === 0 ? 'Keine Konten vorhanden' : 'Keine Konten gefunden' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import ChartOfAccountsService from '@/services/chart-of-accounts.service';
import UserService from '@/services/user.service';
import { showSnackbarMessage } from '@/composables/useSnackbar';

const chartOfAccounts = ref([]);
const selectedChartId = ref('');
const loading = ref(false);
const activating = ref(false);
const currentUser = ref(null);
const accounts = ref([]);
const loadingAccounts = ref(false);
const searchQuery = ref('');
const collapsedClasses = ref({});
const collapsedGroups = ref({});
// Zustand für die Toggle-Buttons
const areAllClassesCollapsed = ref(false);
const areAllGroupsCollapsed = ref(true);

// Berechne das ausgewählte Chart-Objekt basierend auf der ID
const selectedChart = computed(() => {
  if (!selectedChartId.value) return null;
  return chartOfAccounts.value.find(chart => chart.id === selectedChartId.value);
});

// Gefilterte Konten
const filteredAccounts = computed(() => {
  let filtered = accounts.value;

  // Suche anwenden
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(account =>
      account.number.toLowerCase().includes(query) ||
      account.name.toLowerCase().includes(query) ||
      (account.account_group && account.account_group.toLowerCase().includes(query)) ||
      (account.account_class && account.account_class.toLowerCase().includes(query))
    );
  }

  // Sortieren nach Kontonummer
  filtered = [...filtered].sort((a, b) => {
    // Numerischer Vergleich der Kontonummern
    return parseInt(a.number) - parseInt(b.number);
  });

  return filtered;
});

// Ermittelt, welche Klassen Suchergebnisse enthalten
const classesWithSearchResults = computed(() => {
  if (!searchQuery.value) return {};

  const result = {};

  // Iteriert über jede Kontenklasse in den gruppierten Konten
  groupedAccounts.value.forEach(group => {
    // Prüft, ob es in der Klasse Kontengruppen mit Suchergebnissen gibt
    const hasResults = group.accountGroups.some(accountGroup => accountGroup.accounts.length > 0);

    if (hasResults) {
      result[group.className] = true;
    }
  });

  return result;
});

// Ermittelt, welche Gruppen Suchergebnisse enthalten
const groupsWithSearchResults = computed(() => {
  if (!searchQuery.value) return {};

  const result = {};

  // Iteriert über jede Kontenklasse und deren Gruppen
  groupedAccounts.value.forEach(group => {
    group.accountGroups.forEach(accountGroup => {
      // Prüft, ob die Gruppe Suchergebnisse enthält
      if (accountGroup.accounts.length > 0) {
        result[accountGroup.groupKey] = true;
      }
    });
  });

  return result;
});

// Nach Kontenklasse gruppierte Konten
const groupedAccounts = computed(() => {
  const sortedAccounts = [...filteredAccounts.value].sort((a, b) => {
    return parseInt(a.number) - parseInt(b.number);
  });

  const classes = {};

  // Erste Gruppierungsebene: account_class
  sortedAccounts.forEach(account => {
    const className = account.account_class || 'Ohne Klasse';

    if (!classes[className]) {
      classes[className] = {
        accounts: [],
        groups: {}
      };
      // Account-Class ist standardmäßig ausgeklappt
      if (collapsedClasses.value[className] === undefined) {
        collapsedClasses.value[className] = false;
      }
    }

    // Zweite Gruppierungsebene: account_group
    const groupName = account.account_group || 'Ohne Gruppe';

    if (!classes[className].groups[groupName]) {
      classes[className].groups[groupName] = [];

      // Kontengruppen sind standardmäßig zugeklappt
      const groupKey = `${className}-${groupName}`;
      if (collapsedGroups.value[groupKey] === undefined) {
        collapsedGroups.value[groupKey] = true;
      }
    }

    classes[className].groups[groupName].push(account);
  });

  // Hilfsfunktion, um Kontonummer mit führenden Nullen zu formatieren (4-stellig)
  const formatAccountNumber = (number) => {
    return number.toString().padStart(4, '0');
  };

  // Formatiere die verschachtelten Gruppen für die Anzeige
  return Object.entries(classes).map(([className, data]) => {
    const accountGroups = Object.entries(data.groups).map(([groupName, accounts]) => {
      // Sortiere Konten innerhalb jeder Gruppe nach Kontonummern
      const sortedAccounts = [...accounts].sort((a, b) => {
        return parseInt(a.number) - parseInt(b.number);
      });

      // Berechne den exakten Kontonummernbereich für diese Gruppe (ohne Rundung)
      const minAccountNumber = sortedAccounts.length > 0 ? parseInt(sortedAccounts[0].number) : 0;
      const maxAccountNumber = sortedAccounts.length > 0 ? parseInt(sortedAccounts[sortedAccounts.length - 1].number) : 0;

      // Für Kontengruppen: Wenn nur ein Konto vorhanden ist, zeige nur diese Nummer an, sonst zeige Range
      let accountRange = '';
      if (sortedAccounts.length === 0) {
        accountRange = '';
      } else if (sortedAccounts.length === 1 || minAccountNumber === maxAccountNumber) {
        accountRange = formatAccountNumber(minAccountNumber);
      } else {
        accountRange = `${formatAccountNumber(minAccountNumber)}-${formatAccountNumber(maxAccountNumber)}`;
      }

      return {
        groupName,
        accounts: sortedAccounts,
        groupKey: `${className}-${groupName}`,
        // Speichere die niedrigste Kontonummer für die Sortierung der Gruppen
        lowestAccountNumber: minAccountNumber,
        // Speichere den formatierten Kontonummernbereich
        accountRange
      };
    })
      // Sortiere die Gruppen nach der niedrigsten Kontonummer in jeder Gruppe
      .sort((a, b) => a.lowestAccountNumber - b.lowestAccountNumber);

    // Niedrigste und höchste Kontonummer in dieser Klasse für die Bereichsanzeige
    let minClassNumber = Number.MAX_SAFE_INTEGER;
    let maxClassNumber = 0;

    accountGroups.forEach(group => {
      const groupMin = group.lowestAccountNumber;
      const groupMax = group.accounts.length > 0 ?
        parseInt(group.accounts[group.accounts.length - 1].number) : 0;

      minClassNumber = Math.min(minClassNumber, groupMin);
      maxClassNumber = Math.max(maxClassNumber, groupMax);
    });

    // Für Kontenklassen: Runde die Bereichswerte auf tausender
    const roundedClassMin = minClassNumber !== Number.MAX_SAFE_INTEGER ?
      Math.floor(minClassNumber / 1000) * 1000 : 0;
    const roundedClassMax = maxClassNumber > 0 ?
      Math.ceil(maxClassNumber / 1000) * 1000 : 0;

    // Formatiere die Klassenbereiche auch mit führenden Nullen
    let classAccountRange = '';
    if (accountGroups.length === 0) {
      classAccountRange = '';
    } else if (roundedClassMin === roundedClassMax) {
      classAccountRange = formatAccountNumber(roundedClassMin);
    } else {
      classAccountRange = `${formatAccountNumber(roundedClassMin)}-${formatAccountNumber(roundedClassMax)}`;
    }

    const lowestClassNumber = accountGroups.length > 0 ?
      accountGroups[0].lowestAccountNumber : Number.MAX_SAFE_INTEGER;

    return {
      className,
      accountGroups,
      lowestClassNumber,
      classAccountRange
    };
  })
    // Sortiere die Klassen nach der niedrigsten Kontonummer
    .sort((a, b) => a.lowestClassNumber - b.lowestClassNumber);
});

// Funktion zum Ein- oder Ausklappen aller Klassen
const toggleAllClasses = () => {
  // Toggle zwischen den Zuständen
  areAllClassesCollapsed.value = !areAllClassesCollapsed.value;

  // Alle Klassen entsprechend ein- oder ausklappen
  groupedAccounts.value.forEach(group => {
    collapsedClasses.value[group.className] = areAllClassesCollapsed.value;
  });
};

// Funktion zum Ein- oder Ausklappen aller Gruppen
const toggleAllGroups = () => {
  // Toggle zwischen den Zuständen
  areAllGroupsCollapsed.value = !areAllGroupsCollapsed.value;

  // Alle Gruppen entsprechend ein- oder ausklappen
  groupedAccounts.value.forEach(group => {
    group.accountGroups.forEach(accountGroup => {
      collapsedGroups.value[accountGroup.groupKey] = areAllGroupsCollapsed.value;
    });
  });
};

onMounted(async () => {
  await fetchCurrentUser();
  await fetchChartOfAccounts();
});

watch(selectedChartId, async (newVal) => {
  if (newVal) {
    await fetchAccounts(newVal);
  }
});

watch(searchQuery, (newVal) => {
  if (newVal) {
    // Klappt alle Klassen und Gruppen mit Suchergebnissen aus
    Object.keys(classesWithSearchResults.value).forEach(className => {
      collapsedClasses.value[className] = false;
    });
    Object.keys(groupsWithSearchResults.value).forEach(groupKey => {
      collapsedGroups.value[groupKey] = false;
    });
  } else {
    // Wenn die Suche gelöscht wird, klappen wir alles wieder zu
    // Klassen standardmäßig ausgeklappt, Gruppen standardmäßig zugeklappt
    groupedAccounts.value.forEach(group => {
      // Die Hauptkategorien (Klassen) standardmäßig ausgeklappt lassen
      collapsedClasses.value[group.className] = false;

      // Alle Gruppen wieder zuklappen
      group.accountGroups.forEach(accountGroup => {
        collapsedGroups.value[accountGroup.groupKey] = true;
      });
    });
  }
});

const fetchCurrentUser = async () => {
  try {
    currentUser.value = await UserService.getCurrentUser();
  } catch (error) {
    console.error('Fehler beim Laden des aktuellen Benutzers:', error);
    showSnackbarMessage('Fehler beim Laden des Benutzerprofils', 'error');
  }
};

const fetchChartOfAccounts = async () => {
  try {
    loading.value = true;
    chartOfAccounts.value = await ChartOfAccountsService.getAll();

    if (chartOfAccounts.value.length > 0) {
      if (currentUser.value?.chart_of_accounts_id) {
        selectedChartId.value = currentUser.value.chart_of_accounts_id;
      } else {
        selectedChartId.value = chartOfAccounts.value[0].id;
      }
    }
  } catch (error) {
    console.error('Fehler beim Laden der Kontenrahmen:', error);
    showSnackbarMessage('Fehler beim Laden der Kontenrahmen', 'error');
  } finally {
    loading.value = false;
  }
};

const fetchAccounts = async (chartId) => {
  if (!chartId) return;

  try {
    loadingAccounts.value = true;
    accounts.value = await ChartOfAccountsService.getAccounts(chartId);
  } catch (error) {
    console.error(`Fehler beim Laden der Konten für Kontenrahmen ${chartId}:`, error);
    showSnackbarMessage('Fehler beim Laden der Konten', 'error');
    accounts.value = [];
  } finally {
    loadingAccounts.value = false;
  }
};

const handleChartChange = (event) => {
  selectedChartId.value = event.target.value;
};

const isActiveChart = (chartId) => {
  return currentUser.value?.chart_of_accounts_id === chartId;
};

const getAccountTypeName = (type) => {
  const types = {
    'ASSET': 'Aktivkonto',
    'LIABILITY': 'Passivkonto',
    'EQUITY': 'Eigenkapitalkonto',
    'REVENUE': 'Ertragskonto',
    'EXPENSE': 'Aufwandskonto'
  };

  return types[type] || type;
};

const activateChart = async () => {
  if (!selectedChart.value || isActiveChart(selectedChart.value.id)) return;

  activating.value = true;

  try {
    await UserService.updateUser({
      chart_of_accounts_id: selectedChart.value.id
    });

    await fetchCurrentUser();

    showSnackbarMessage(`Kontenrahmen "${selectedChart.value.name}" erfolgreich aktiviert`, 'success');
  } catch (error) {
    console.error('Fehler beim Aktivieren des Kontenrahmens:', error);
    showSnackbarMessage('Fehler beim Aktivieren des Kontenrahmens', 'error');
  } finally {
    activating.value = false;
  }
};

const toggleClassCollapse = (className) => {
  collapsedClasses.value[className] = !collapsedClasses.value[className];
};

const toggleGroupCollapse = (groupKey) => {
  collapsedGroups.value[groupKey] = !collapsedGroups.value[groupKey];
};
</script>

<style scoped></style>