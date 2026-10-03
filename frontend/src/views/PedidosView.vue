<template>
  <section>
    <h2>Pedidos</h2>
    <AlertMessage :message="error" />
    <form class="card form-grid" novalidate @submit.prevent="guardar">
      <BaseSelect v-model="form.cliente_id" label="Cliente" placeholder="Seleccione un cliente"
        :options="opcionesClientes" :error="errores.cliente_id" />
      <BaseSelect v-model="form.producto_id" label="Producto" placeholder="Seleccione un producto"
        :options="opcionesProductos" :error="errores.producto_id" />
      <BaseInput v-model="form.cantidad" label="Cantidad" type="number" step="1" min="1" :error="errores.cantidad" />
      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">Crear pedido</BaseButton>
      </div>
    </form>

    <DataTable :rows="pedidos" :columns="columns">
      <template #actions="{ row }">
        <select :value="row.estado" :aria-label="`Estado del pedido ${row.id}`" @change="cambiarEstado(row, $event.target.value)">
          <option v-for="e in estados" :key="e" :value="e">{{ e }}</option>
        </select>
        <BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { clientesApi } from '../api/clientes'
import { productosApi } from '../api/productos'
import { pedidosApi } from '../api/pedidos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import BaseSelect from '../components/BaseSelect.vue'
import DataTable from '../components/DataTable.vue'

const estados = ['pendiente', 'pagado', 'enviado', 'cancelado']
const pedidos = ref([])
const clientes = ref([])
const productos = ref([])
const error = ref('')
const guardando = ref(false)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'cliente', label: 'Cliente' },
  { key: 'producto', label: 'Producto' },
  { key: 'cantidad', label: 'Cantidad' },
  { key: 'total', label: 'Total', format: (v) => `Q${Number(v).toFixed(2)}` },
  { key: 'estado', label: 'Estado' },
]

const opcionesClientes = computed(() => clientes.value.map((c) => ({ value: c.id, label: c.nombre })))
const opcionesProductos = computed(() =>
  productos.value
    .filter((p) => p.activo)
    .map((p) => ({ value: p.id, label: `${p.nombre} — Q${p.precio.toFixed(2)} (stock ${p.stock})` })),
)

const vacio = () => ({ cliente_id: '', producto_id: '', cantidad: 1 })
const sinErrores = () => ({ cliente_id: '', producto_id: '', cantidad: '' })
const form = reactive(vacio())
const errores = reactive(sinErrores())

function validar() {
  Object.assign(errores, sinErrores())
  if (form.cliente_id === '') errores.cliente_id = 'Seleccione un cliente.'
  if (form.producto_id === '') errores.producto_id = 'Seleccione un producto.'
  if (!Number.isInteger(Number(form.cantidad)) || Number(form.cantidad) < 1)
    errores.cantidad = 'La cantidad debe ser un entero mayor que 0.'
  return !Object.values(errores).some(Boolean)
}

async function cargar() {
  try {
    const [p, c, pr] = await Promise.all([pedidosApi.listar(), clientesApi.listar(), productosApi.listar()])
    pedidos.value = p.data
    clientes.value = c.data
    productos.value = pr.data
  } catch (err) {
    error.value = err.message
  }
}

async function guardar() {
  error.value = ''
  if (!validar()) return
  guardando.value = true
  try {
    await pedidosApi.crear({
      cliente_id: Number(form.cliente_id),
      producto_id: Number(form.producto_id),
      cantidad: Number(form.cantidad),
    })
    Object.assign(form, vacio())
    await cargar()
  } catch (err) {
    error.value = err.message
  } finally {
    guardando.value = false
  }
}

async function cambiarEstado(pedido, estado) {
  error.value = ''
  try {
    await pedidosApi.actualizar(pedido.id, { estado })
  } catch (err) {
    error.value = err.message
  }
  await cargar() // refresca tabla y stock; si hubo error, el selector vuelve al valor real
}

async function eliminar(pedido) {
  if (!window.confirm(`¿Eliminar el pedido ${pedido.id}?`)) return
  error.value = ''
  try {
    await pedidosApi.eliminar(pedido.id)
    await cargar()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(cargar)
</script>
