<template>
  <section>
    <h2>Clientes</h2>
    <AlertMessage :message="error" />
    <form class="card form-grid" novalidate @submit.prevent="guardar">
      <BaseInput v-model="form.nombre" label="Nombre" :error="errores.nombre" />
      <BaseInput v-model="form.correo" label="Correo" type="email" :error="errores.correo" />
      <BaseInput v-model="form.telefono" label="Teléfono" :error="errores.telefono" />
      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">
          {{ editando ? 'Guardar cambios' : 'Crear cliente' }}
        </BaseButton>
        <BaseButton v-if="editando" variant="secondary" @click="limpiar">Cancelar</BaseButton>
      </div>
    </form>

    <DataTable :rows="clientes" :columns="columns">
      <template #actions="{ row }">
        <BaseButton variant="secondary" @click="editar(row)">Editar</BaseButton>
        <BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { clientesApi } from '../api/clientes'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const clientes = ref([])
const error = ref('')
const guardando = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'correo', label: 'Correo' },
  { key: 'telefono', label: 'Teléfono' },
]

const vacio = () => ({ nombre: '', correo: '', telefono: '' })
const form = reactive(vacio())
const errores = reactive(vacio())

function validar() {
  Object.assign(errores, vacio())
  if (!form.nombre.trim()) errores.nombre = 'Escriba el nombre.'
  if (!form.correo.trim()) errores.correo = 'Escriba el correo.'
  else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.correo.trim())) errores.correo = 'El correo no es válido.'
  return !Object.values(errores).some(Boolean)
}

function limpiar() {
  Object.assign(form, vacio())
  Object.assign(errores, vacio())
  editando.value = false
  idEditando.value = null
}

async function cargar() {
  try {
    clientes.value = (await clientesApi.listar()).data
  } catch (err) {
    error.value = err.message
  }
}

async function guardar() {
  error.value = ''
  if (!validar()) return
  guardando.value = true
  try {
    if (editando.value) await clientesApi.actualizar(idEditando.value, form)
    else await clientesApi.crear(form)
    limpiar()
    await cargar()
  } catch (err) {
    error.value = err.message
  } finally {
    guardando.value = false
  }
}

function editar(c) {
  Object.assign(form, { nombre: c.nombre, correo: c.correo, telefono: c.telefono || '' })
  editando.value = true
  idEditando.value = c.id
}

async function eliminar(c) {
  if (!window.confirm(`¿Eliminar a ${c.nombre}?`)) return
  error.value = ''
  try {
    await clientesApi.eliminar(c.id)
    await cargar()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(cargar)
</script>
