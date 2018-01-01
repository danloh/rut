<template>
  <div class="edit-page">
    <h3 class="title"> Edit Read-up-Tips:
      <router-link class="title" :to="'/readuplist/' + rutId">{{rutTitle}}</router-link>
    </h3>
    <el-form class="edit-form" :model="editForm" :rules="rules" ref="editForm" label-width="120px" size="mini">
      <el-form-item label="Change Order" prop="order">
        <el-input v-model="editForm.order"></el-input>
      </el-form-item>
      <el-form-item label="Edit Tips" prop="tips">
        <!-- <el-input type="textarea" v-model="editForm.tips"></el-input> -->
        <quill-editor v-model="editForm.tips"
                      ref="TextEditor"
                      class="quill-editor">
        </quill-editor>
      </el-form-item>
      <el-form-item label="Reminder" prop="spoiler">
        <el-radio-group v-model="editForm.spoiler">
          <el-radio-button label="No Spoiler"></el-radio-button>
          <el-radio-button label="Spoiler Ahead"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="success" size="medium" @click="onEdit('editForm', editForm)">Edit and Submit</el-button>
        <!-- <el-button @click="resetForm('editForm')">Reset</el-button> -->
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <el-button type="danger" plain size="mini" @click="showDialog = true">Delete Tips</el-button>
      </el-form-item>
    </el-form>
    <!-- confirm delete dialog -->
    <el-dialog title="Confirm Delete Tips?" :visible.sync="showDialog" width="30%">
      <span>Confirm Delete? Can not recover</span>
      <span slot="footer" class="dialog-footer">
        <el-button size="mini" @click="showDialog = false">Cancel</el-button>
        <el-button type="danger" size="mini" @click="delTips">Confirm Delete</el-button>
      </span>
    </el-dialog>
    <!-- dialog end -->
  </div>
</template>

<script>
import { editTips, deleteTips } from '@/api/api'
import { checkAuth } from '@/util/auth'
import { trimValid } from '@/util/filters'

export default {
  name: 'edit-tips',
  title: 'Edit Tip',
  data () {
    return {
      editForm: {
        order: '',
        tips: '',
        spoiler: ''
      },
      rules: {
        order: [
          { required: true, message: 'Required', trigger: 'blur' }
        ],
        tips: [
          { required: true, validator: trimValid, message: 'Required', trigger: 'blur' }
        ]
      },
      showDialog: false,
      rutId: null,
      rutTitle: null,
      canEdit: false
    }
  },
  methods: {
    onEdit (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid && checkAuth() && this.canEdit) {
          let data = {
            order: form.order,
            tips: form.tips.trim(),
            spoiler: form.spoiler
          }
          let cid = this.$route.params.id
          editTips(cid, data)
          .then(() => {
            let id = this.rutId
            this.$router.push(`/readuplist/${id}`)
          })
        } else {
          this.$message({
            showClose: true,
            message: 'error!! Please Check'
          })
          return false
        }
      })
    },
    delTips () {
      let cid = this.$route.params.id
      deleteTips(cid).then(() => {
        let id = this.rutId
        this.$router.push(`/readuplist/${id}`)
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    loadTipsData () {
      let rut = this.$store.getters.rutDetail
      let tips = this.$store.getters.rutDetail.tips
      let tip = tips.filter((element) => {
        let rcid = this.$route.params.id
        return Number(element.cid) === Number(rcid)
      })[0]
      this.editForm.order = tip.order
      this.editForm.tips = tip.tip
      this.editForm.spoiler = tip.spoiler ? 'Spoiler Ahead' : 'No Spoiler'
      this.rutId = rut.id
      this.rutTitle = rut.title
      let creatorID = rut.creator.id
      let currentUserID = this.$store.getters.currentUserID
      this.canEdit = Number(creatorID) === Number(currentUserID)
    }
  },
  created () {
    this.loadTipsData()
  }
}
</script>

<style lang="stylus" scoped>
.edit-page
  padding 10px 120px 10px 80px
  position relative
  .edit-form
    padding 20px
    border 1px dotted #689f38
  .title
    margin-bottom 20px
</style>