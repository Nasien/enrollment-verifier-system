import { useEffect, useState } from 'react'
import { Alert, Button, Card, Col, Form, Row } from 'react-bootstrap'
import Layout from '../components/Layout'
import api from '../api/client'

const initialMeta = {
  hei_name: '', academic_year: '', semester: '', scholarship: '', batch: ''
}

export default function UploadPage() {
  const [meta, setMeta] = useState(initialMeta)
  const [granteeFile, setGranteeFile] = useState(null)
  const [enrollmentFile, setEnrollmentFile] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [history, setHistory] = useState([])
  const [selectedGranteeUpload, setSelectedGranteeUpload] = useState('')
  const [selectedEnrollmentUpload, setSelectedEnrollmentUpload] = useState('')

  const loadHistory = () => api.get('/uploads/history').then((res) => setHistory(res.data))
  useEffect(() => { loadHistory() }, [])

  const handleMeta = (e) => setMeta({ ...meta, [e.target.name]: e.target.value })

  const uploadGrantee = async () => {
    const form = new FormData()
    Object.entries(meta).forEach(([k, v]) => form.append(k, v))
    form.append('file', granteeFile)
    const res = await api.post('/uploads/grantee', form)
    setMessage(res.data.message)
    loadHistory()
  }

  const uploadEnrollment = async () => {
    const form = new FormData()
    form.append('hei_name', meta.hei_name)
    form.append('academic_year', meta.academic_year)
    form.append('semester', meta.semester)
    form.append('file', enrollmentFile)
    const res = await api.post('/uploads/enrollment', form)
    setMessage(res.data.message)
    loadHistory()
  }

  const runVerification = async () => {
    const res = await api.post('/verification/run', {
      grantee_upload_id: selectedGranteeUpload,
      enrollment_upload_id: selectedEnrollmentUpload,
      threshold: 88,
    })
    setMessage(`Verification completed. Session ID: ${res.data.session_id}`)
  }

  const granteeUploads = history.filter((x) => x.upload_type === 'grantee')
  const enrollmentUploads = history.filter((x) => x.upload_type === 'enrollment')

  return (
    <Layout>
      <h2 className="page-title mb-4">Upload and Verify</h2>
      {message && <Alert variant="success">{message}</Alert>}
      {error && <Alert variant="danger">{error}</Alert>}
      <Row className="g-4">
        <Col lg={6}>
          <Card className="card-soft p-3 h-100">
            <h5>Metadata</h5>
            <Row className="g-3">
              {['hei_name', 'academic_year', 'semester', 'scholarship', 'batch'].map((name) => (
                <Col md={name === 'hei_name' ? 12 : 6} key={name}>
                  <Form.Label className="text-capitalize">{name.replace('_', ' ')}</Form.Label>
                  <Form.Control name={name} value={meta[name]} onChange={handleMeta} />
                </Col>
              ))}
            </Row>
          </Card>
        </Col>
        <Col lg={6}>
          <Card className="card-soft p-3 h-100">
            <h5>Upload Files</h5>
            <Form.Group className="mb-3">
              <Form.Label>Grantee masterlist</Form.Label>
              <Form.Control type="file" accept=".xlsx,.xls,.csv" onChange={(e) => setGranteeFile(e.target.files[0])} />
            </Form.Group>
            <Button className="me-2 mb-3" onClick={() => uploadGrantee().catch((e) => setError(e.response?.data?.detail || 'Upload failed'))} disabled={!granteeFile}>Upload Grantee File</Button>
            <Form.Group className="mb-3">
              <Form.Label>Enrollment list</Form.Label>
              <Form.Control type="file" accept=".xlsx,.xls,.csv" onChange={(e) => setEnrollmentFile(e.target.files[0])} />
            </Form.Group>
            <Button variant="secondary" onClick={() => uploadEnrollment().catch((e) => setError(e.response?.data?.detail || 'Upload failed'))} disabled={!enrollmentFile}>Upload Enrollment File</Button>
          </Card>
        </Col>
      </Row>

      <Card className="card-soft p-3 mt-4">
        <h5>Run Verification</h5>
        <Row className="g-3 align-items-end">
          <Col md={5}>
            <Form.Label>Select grantee upload</Form.Label>
            <Form.Select value={selectedGranteeUpload} onChange={(e) => setSelectedGranteeUpload(e.target.value)}>
              <option value="">Choose...</option>
              {granteeUploads.map((item) => <option value={item.id} key={item.id}>{item.hei_name} | {item.academic_year} | {item.batch}</option>)}
            </Form.Select>
          </Col>
          <Col md={5}>
            <Form.Label>Select enrollment upload</Form.Label>
            <Form.Select value={selectedEnrollmentUpload} onChange={(e) => setSelectedEnrollmentUpload(e.target.value)}>
              <option value="">Choose...</option>
              {enrollmentUploads.map((item) => <option value={item.id} key={item.id}>{item.hei_name} | {item.academic_year} | {item.semester}</option>)}
            </Form.Select>
          </Col>
          <Col md={2}>
            <Button className="w-100" onClick={() => runVerification().catch((e) => setError(e.response?.data?.detail || 'Verification failed'))}>Run</Button>
          </Col>
        </Row>
      </Card>
    </Layout>
  )
}
