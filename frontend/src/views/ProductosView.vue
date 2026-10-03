<template>
  <section>
    <h2>Productos</h2>
    <AlertMessage :message="error" />
    <form class="card form-grid" novalidate @submit.prevent="guardar">
      <BaseInput v-model="form.nombre" label="Nombre" :error="errores.nombre" />
      <BaseInput v-model="form.descripcion" label="Descripción" :error="errores.descripcion" />
      <BaseInput v-model="form.precio" label="Precio (Q)" type="number" step="0.01" min="0" :error="errores.precio" />
      <BaseInput v-model="form.stock" label="Stock" type="number" step="1" min="0" :error="errores.stock" />
      <label class="field field--check">
        <input v-model="form.activo" type="checkbox" />
        <span>Producto activo</span>
      </label>
      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">
          {{ editando ? 'Guardar cambios' : 'Crear producto' }}
        </BaseButton>
        <BaseButton v-if="editando" variant="secondary" @click="limpiar">Cancelar</BaseButton>
      </div>
    </form>

    <DataTable :rows="productos" :columns="columns">
      <template #actions="{ row }">
        <BaseButton variant="secondary" @click="editar(row)">Editar</BaseButton>
        <BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { productosApi } from '../api/productos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const productos = ref([])
const error = ref('')
const guardando = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'precio', label: 'Precio', format: (v) => `Q${Number(v).toFixed(2)}` },
  { key: 'stock', label: 'Stock' },
  { key: 'activo', label: 'Activo', format: (v) => (v ? 'Sí' : 'No') },
]

const vacio = () => ({ nombre: '', descripcion: '', precio: '', stock: '', activo: true })
const sinErrores = () => ({ nombre: '', descripcion: '', precio: '', stock: '' })
const form = reactive(vacio())
const errores = reactive(sinErrores())

function validar() {
  Object.assign(errores, sinErrores())
  if (!form.nombre.trim()) errores.nombre = 'Escriba el nombre.'
  if (form.descripcion.length > 300) errores.descripcion = 'Máximo 300 caracteres.'
  if (form.precio === '' || Number.isNaN(Number(form.precio)) || Number(form.precio) < 0)
    errores.precio = 'Ingrese un precio mayor o igual a 0.'
  if (form.stock === '' || !Number.isInteger(Number(form.stock)) || Number(form.stock) < 0)
    errores.stock = 'Ingrese un entero mayor o igual a 0.'
  return !Object.values(errores).some(Boolean)
}

function limpiar() {
  Object.assign(form, vacio())
  Object.assign(errores, sinErrores())
  editando.value = false
  idEditando.value = null
}

async function cargar() {
  try {
    productos.value = (await productosApi.listar()).data
  } catch (err) {
    error.value = err.message
  }
}

async function guardar() {
  error.value = ''
  if (!validar()) return
  guardando.value = true
  const payload = { ...form, precio: Number(form.precio), stock: Number(form.stock) }
  try {
    if (editando.value) await productosApi.actualizar(idEditando.value, payload)
    else await productosApi.crear(payload)
    limpiar()
    await cargar()
  } catch (err) {
    error.value = err.message
  } finally {
    guardando.value = false
  }
}

function editar(p) {
  Object.assign(form, {
    nombre: p.nombre,
    descripcion: p.descripcion || '',
    precio: p.precio,
    stock: p.stock,
    activo: p.activo,
  })
  editando.value = true
  idEditando.value = p.id
}

async function eliminar(p) {
  if (!window.confirm(`¿Eliminar ${p.nombre}?`)) return
  error.value = ''
  try {
    await productosApi.eliminar(p.id)
    await cargar()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(cargar)
</script>
