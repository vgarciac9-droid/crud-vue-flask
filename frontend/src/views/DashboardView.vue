<template>
  <section>
    <h2>Resumen</h2>
    <AlertMessage :message="error" />
    <div class="stats">
      <RouterLink v-for="s in stats" :key="s.to" :to="s.to" class="card stat">
        <strong>{{ s.value }}</strong>
        <span>{{ s.label }}</span>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { clientesApi } from '../api/clientes'
import { productosApi } from '../api/productos'
import { pedidosApi } from '../api/pedidos'
import AlertMessage from '../components/AlertMessage.vue'

const error = ref('')
const total = ref({ clientes: 0, productos: 0, pedidos: 0 })
const stats = computed(() => [
  { to: '/clientes', label: 'Clientes registrados', value: total.value.clientes },
  { to: '/productos', label: 'Productos en catálogo', value: total.value.productos },
  { to: '/pedidos', label: 'Pedidos', value: total.value.pedidos },
])

onMounted(async () => {
  try {
    const [c, p, o] = await Promise.all([clientesApi.listar(), productosApi.listar(), pedidosApi.listar()])
    total.value = { clientes: c.data.length, productos: p.data.length, pedidos: o.data.length }
  } catch (err) {
    error.value = err.message
  }
})
</script>
