import type { Locale } from './locales';
import siteBase from '../data/site.json';

type ResearchArea = (typeof siteBase.researchAreas)[number];
type ArchLayer = (typeof siteBase.architecture.layers)[number];
type Project = (typeof siteBase.projects)[number];

type LocalizedSite = {
  name: string;
  shortName: string;
  affiliation: string;
  campus: string;
  location: string;
  tagline: string;
  headline: string;
  description: string;
  email: string;
  pi: { name: string; shortName?: string; title: string };
  researchAreas: ResearchArea[];
  architecture: {
    title: string;
    summary: string;
    layers: ArchLayer[];
  };
  heroImage: string;
  projects: Project[];
};

const zhSite: LocalizedSite = {
  name: '计算、通信与能源系统优化实验室',
  shortName: 'C2E',
  affiliation: '香港科技大学（广州）信息枢纽物联网学域',
  campus: '香港科技大学（广州）',
  location: '中国广东广州',
  tagline: '计算、通信与能源系统优化',
  headline: '致力于网络化系统的优化',
  description:
    '我们通过数学建模与优化提升工程系统性能——从云与边缘计算，到无线网络与智慧能源系统。',
  email: siteBase.email,
  pi: {
    name: 'Prof. Danny H.K. Tsang',
    shortName: 'Danny Tsang',
    title: '教授，IEEE Fellow，HKIE Fellow',
  },
  researchAreas: [
    {
      id: 'wireless',
      title: '无线通信',
      summary:
        '下一代无线网络、IRS 辅助 MEC、无线传能、天线设计、NOMA、Wi-Fi 网络等。',
      image: '/images/research/wireless.jpg',
    },
    {
      id: 'cloud-edge',
      title: '云 / 边缘计算',
      summary: '面向云与移动边缘系统的资源管理、任务卸载与性能优化。',
      image: '/images/research/cloud-edge.jpg',
    },
    {
      id: 'online-algorithms',
      title: '在线算法设计',
      summary: '不确定环境下资源分配的竞争算法与机制设计。',
      image: '/images/research/online-algorithms.jpg',
    },
    {
      id: 'smart-grids',
      title: '智能电网',
      summary: '电动汽车充电、可再生能源管理、调频与电力网络定价。',
      image: '/images/research/smart-grids.jpg',
    },
  ],
  architecture: {
    title: '一个统一目标——更智慧、更清洁的世界',
    summary:
      '四大研究方向构成同一系统的分层架构：能源作为基础设施，无线作为连接纽带，云与边缘作为计算平面，在线算法作为贯通各层的决策层。',
    layers: [
      {
        id: 'online-algorithms',
        role: '决策',
        title: '在线算法设计',
        blurb: '在不确定条件下优化整栈资源与决策。',
      },
      {
        id: 'cloud-edge',
        role: '计算',
        title: '云 / 边缘计算',
        blurb: '在时延与能耗允许的地方部署智能。',
      },
      {
        id: 'wireless',
        role: '连接',
        title: '无线通信',
        blurb: '在空中传递信息——并越来越多地传递能量。',
      },
      {
        id: 'smart-grids',
        role: '能源',
        title: '智能电网',
        blurb: '支撑网络化系统可持续发展的能源基础。',
      },
    ],
  },
  heroImage: siteBase.heroImage,
  projects: [
    {
      title: '工业多网关 Wi-Fi Mesh 流量调度平台',
      summary:
        '本项目面向有线回传受限或成本较高的工业场景，开发基于 OpenWrt 的多网关 Wi-Fi Mesh 平台。系统可动态将互联网流量调度至选定网关，同时保持与标准 Wi-Fi 客户端及通用路由器的兼容性。',
      highlights: [
        '连接级网关选择与跨多互联网网关的流量调度。',
        '基于 Netfilter/NFQUEUE、路由、NAT 状态与 Netlink 控制的内核与用户态报文处理流水线。',
        '高效非对称处理：出站 LAN 到互联网报文进行分类与调度，回程流量沿已建立路由转发而无需重复应用层过滤。',
        '通过真实网络测量、流量日志与多网关测试场景完成原型验证。',
      ],
      deliverables: [
        '可用的 OpenWrt 多网关 Mesh 原型。',
        '网关选择与按流转发模块。',
        '内核流状态表与基于 C 的 Netlink 控制软件。',
        '实验评估工具、测量数据集与技术文档。',
      ],
    },
    {
      title: '面向蜂窝使能 Wi-Fi Mesh 网络的成本感知负载均衡与无缝移动性',
      summary:
        '本项目研究将多台蜂窝使能路由器作为大规模 Wi-Fi Mesh 网络的互联网网关。我们构建了集中控制架构，在兼顾蜂窝流量配额与多跳转发成本的同时均衡网关负载，并支持站点移动而不中断已有 TCP 连接。',
      highlights: [
        '在通用 Linux 路由器上实现的 SDN 启发控制架构。',
        '二次规划辅助负载均衡（QPLB），联合优化网关配额使用与 Mesh 转发成本。',
        '多蜂窝网关并发利用。',
        '按需按连接转发，客户端在 Mesh 节点间漫游时保持 TCP 会话不中断。',
        '无需修改客户端设备或底层 Wi-Fi 标准。',
        '评估显示，相对代表性基线，蜂窝配额失衡降低 58%–83%，中位字节加权跳数降低 34%。',
      ],
      deliverables: [
        'QPLB 优化算法与仿真框架。',
        '基于现成无线路由器的完整可用原型。',
        '无缝漫游与按连接转发机制。',
        '仿真与原型评估结果。',
        '授权专利 CN118233979B：一种在Mesh网络中无缝漫游的方法及系统（A Method and a System for Seamless Roaming in Mesh Network）。',
        '授权专利 CN118488512B：一种局域网中多网关处理数据的方法及系统（A Method and a System for Multi-Gateway Data Processing in LAN）。',
        '授权专利 CN118524445B：一种Mesh网络中流量负载均衡方法和装置（A Method and an Equipment for Traffic Load-Balancing in Mesh Network）。',
      ],
    },
  ],
};

export function getSite(locale: Locale): LocalizedSite {
  if (locale === 'zh-cn') return zhSite;
  return siteBase as LocalizedSite;
}

export function htmlLang(locale: Locale): string {
  return locale === 'zh-cn' ? 'zh-CN' : 'en';
}

export function dateLocale(locale: Locale): string {
  return locale === 'zh-cn' ? 'zh-CN' : 'en-US';
}
