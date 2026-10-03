<template>
  <label class="field">
    <span>{{ label }}</span>
    <select :value="modelValue" @change="$emit('update:modelValue', $event.target.value)">
      <option disabled value="">{{ placeholder }}</option>
      <option v-for="o in options" :key="o.value" :value="o.value">{{ o.label }}</option>
    </select>
    <small v-if="error" class="field__error">{{ error }}</small>
  </label>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, default: () => [] },
  placeholder: { type: String, default: 'Seleccione una opción' },
  error: { type: String, default: '' },
})
defineEmits(['update:modelValue'])
</script>
