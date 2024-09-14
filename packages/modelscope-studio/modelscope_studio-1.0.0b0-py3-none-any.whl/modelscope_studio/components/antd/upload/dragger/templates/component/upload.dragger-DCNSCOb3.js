import { g as se, w as E } from "./Index-DJHLa2vN.js";
const H = window.ms_globals.React, oe = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, re = window.ms_globals.React.useEffect, K = window.ms_globals.React.useMemo, C = window.ms_globals.ReactDOM.createPortal, ie = window.ms_globals.antd.Upload;
var B = {
  exports: {}
}, F = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var le = H, ce = Symbol.for("react.element"), ae = Symbol.for("react.fragment"), de = Object.prototype.hasOwnProperty, ue = le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, fe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(e, o, s) {
  var n, i = {}, t = null, r = null;
  s !== void 0 && (t = "" + s), o.key !== void 0 && (t = "" + o.key), o.ref !== void 0 && (r = o.ref);
  for (n in o) de.call(o, n) && !fe.hasOwnProperty(n) && (i[n] = o[n]);
  if (e && e.defaultProps) for (n in o = e.defaultProps, o) i[n] === void 0 && (i[n] = o[n]);
  return {
    $$typeof: ce,
    type: e,
    key: t,
    ref: r,
    props: i,
    _owner: ue.current
  };
}
F.Fragment = ae;
F.jsx = J;
F.jsxs = J;
B.exports = F;
var y = B.exports;
const {
  SvelteComponent: pe,
  assign: q,
  binding_callbacks: M,
  check_outros: me,
  component_subscribe: W,
  compute_slots: _e,
  create_slot: we,
  detach: R,
  element: Y,
  empty: be,
  exclude_internal_props: z,
  get_all_dirty_from_scope: ve,
  get_slot_changes: ge,
  group_outros: he,
  init: ye,
  insert: U,
  safe_not_equal: Ie,
  set_custom_element_data: Q,
  space: xe,
  transition_in: S,
  transition_out: D,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: Re,
  getContext: Ue,
  onDestroy: Se,
  setContext: Fe
} = window.__gradio__svelte__internal;
function A(e) {
  let o, s;
  const n = (
    /*#slots*/
    e[7].default
  ), i = we(
    n,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      o = Y("svelte-slot"), i && i.c(), Q(o, "class", "svelte-1rt0kpf");
    },
    m(t, r) {
      U(t, o, r), i && i.m(o, null), e[9](o), s = !0;
    },
    p(t, r) {
      i && i.p && (!s || r & /*$$scope*/
      64) && Ee(
        i,
        n,
        t,
        /*$$scope*/
        t[6],
        s ? ge(
          n,
          /*$$scope*/
          t[6],
          r,
          null
        ) : ve(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      s || (S(i, t), s = !0);
    },
    o(t) {
      D(i, t), s = !1;
    },
    d(t) {
      t && R(o), i && i.d(t), e[9](null);
    }
  };
}
function Le(e) {
  let o, s, n, i, t = (
    /*$$slots*/
    e[4].default && A(e)
  );
  return {
    c() {
      o = Y("react-portal-target"), s = xe(), t && t.c(), n = be(), Q(o, "class", "svelte-1rt0kpf");
    },
    m(r, a) {
      U(r, o, a), e[8](o), U(r, s, a), t && t.m(r, a), U(r, n, a), i = !0;
    },
    p(r, [a]) {
      /*$$slots*/
      r[4].default ? t ? (t.p(r, a), a & /*$$slots*/
      16 && S(t, 1)) : (t = A(r), t.c(), S(t, 1), t.m(n.parentNode, n)) : t && (he(), D(t, 1, 1, () => {
        t = null;
      }), me());
    },
    i(r) {
      i || (S(t), i = !0);
    },
    o(r) {
      D(t), i = !1;
    },
    d(r) {
      r && (R(o), R(s), R(n)), e[8](null), t && t.d(r);
    }
  };
}
function T(e) {
  const {
    svelteInit: o,
    ...s
  } = e;
  return s;
}
function ke(e, o, s) {
  let n, i, {
    $$slots: t = {},
    $$scope: r
  } = o;
  const a = _e(t);
  let {
    svelteInit: f
  } = o;
  const b = E(T(o)), c = E();
  W(e, c, (d) => s(0, n = d));
  const l = E();
  W(e, l, (d) => s(1, i = d));
  const u = [], h = Ue("$$ms-gr-antd-react-wrapper"), {
    slotKey: m,
    slotIndex: L,
    subSlotIndex: k
  } = se() || {}, v = f({
    parent: h,
    props: b,
    target: c,
    slot: l,
    slotKey: m,
    slotIndex: L,
    subSlotIndex: k,
    onDestroy(d) {
      u.push(d);
    }
  });
  Fe("$$ms-gr-antd-react-wrapper", v), Re(() => {
    b.set(T(o));
  }), Se(() => {
    u.forEach((d) => d());
  });
  function I(d) {
    M[d ? "unshift" : "push"](() => {
      n = d, c.set(n);
    });
  }
  function O(d) {
    M[d ? "unshift" : "push"](() => {
      i = d, l.set(i);
    });
  }
  return e.$$set = (d) => {
    s(17, o = q(q({}, o), z(d))), "svelteInit" in d && s(5, f = d.svelteInit), "$$scope" in d && s(6, r = d.$$scope);
  }, o = z(o), [n, i, c, l, a, f, r, t, I, O];
}
class Oe extends pe {
  constructor(o) {
    super(), ye(this, o, ke, Le, Ie, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, P = window.ms_globals.tree;
function je(e) {
  function o(s) {
    const n = E(), i = new Oe({
      ...s,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, a = t.parent ?? P;
          return a.nodes = [...a.nodes, r], G({
            createPortal: C,
            node: P
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((f) => f.svelteInstance !== n), G({
              createPortal: C,
              node: P
            });
          }), r;
        },
        ...s.props
      }
    });
    return n.set(i), i;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(o);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function De(e) {
  return e ? Object.keys(e).reduce((o, s) => {
    const n = e[s];
    return typeof n == "number" && !Pe.includes(s) ? o[s] = n + "px" : o[s] = n, o;
  }, {}) : {};
}
function X(e) {
  const o = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((n) => {
    e.getEventListeners(n).forEach(({
      listener: t,
      type: r,
      useCapture: a
    }) => {
      o.addEventListener(r, t, a);
    });
  });
  const s = Array.from(e.children);
  for (let n = 0; n < s.length; n++) {
    const i = s[n], t = X(i);
    o.replaceChild(t, o.children[n]);
  }
  return o;
}
function Ne(e, o) {
  e && (typeof e == "function" ? e(o) : e.current = o);
}
const x = oe(({
  slot: e,
  clone: o,
  className: s,
  style: n
}, i) => {
  const t = ne();
  return re(() => {
    var b;
    if (!t.current || !e)
      return;
    let r = e;
    function a() {
      let c = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (c = r.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ne(i, c), s && c.classList.add(...s.split(" ")), n) {
        const l = De(n);
        Object.keys(l).forEach((u) => {
          c.style[u] = l[u];
        });
      }
    }
    let f = null;
    if (o && window.MutationObserver) {
      let c = function() {
        var l;
        r = X(e), r.style.display = "contents", a(), (l = t.current) == null || l.appendChild(r);
      };
      c(), f = new window.MutationObserver(() => {
        var l, u;
        (l = t.current) != null && l.contains(r) && ((u = t.current) == null || u.removeChild(r)), c();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", a(), (b = t.current) == null || b.appendChild(r);
    return () => {
      var c, l;
      r.style.display = "", (c = t.current) != null && c.contains(r) && ((l = t.current) == null || l.removeChild(r)), f == null || f.disconnect();
    };
  }, [e, o, s, n, i]), H.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Ce(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function w(e) {
  return K(() => Ce(e), [e]);
}
function qe(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const We = je(({
  slots: e,
  upload: o,
  showUploadList: s,
  progress: n,
  beforeUpload: i,
  customRequest: t,
  previewFile: r,
  isImageUrl: a,
  itemRender: f,
  iconRender: b,
  data: c,
  onChange: l,
  onValueChange: u,
  onRemove: h,
  fileList: m,
  ...L
}) => {
  const k = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof s == "object", v = qe(s), I = w(i), O = w(t), d = w(n == null ? void 0 : n.format), Z = w(r), V = w(a), $ = w(f), ee = w(b), te = w(c), N = K(() => (m == null ? void 0 : m.map((p) => ({
    ...p,
    name: p.orig_name || p.path,
    uid: p.url || p.path,
    status: "done"
  }))) || [], [m]);
  return /* @__PURE__ */ y.jsx(ie.Dragger, {
    ...L,
    fileList: N,
    data: te || c,
    previewFile: Z,
    isImageUrl: V,
    itemRender: $,
    iconRender: ee,
    onRemove: (p) => {
      h == null || h(p);
      const j = N.findIndex((_) => _.uid === p.uid), g = m.slice();
      g.splice(j, 1), u == null || u(g), l == null || l(g.map((_) => _.path));
    },
    beforeUpload: async (p, j) => {
      if (I && !await I(p, j))
        return !1;
      const g = (await o([p])).filter((_) => _);
      return u == null || u([...m, ...g]), l == null || l([...m.map((_) => _.path), ...g.map((_) => _.path)]), !1;
    },
    customRequest: O,
    progress: n && {
      ...n,
      format: d
    },
    showUploadList: k ? {
      ...v,
      downloadIcon: e["showUploadList.downloadIcon"] ? /* @__PURE__ */ y.jsx(x, {
        slot: e["showUploadList.downloadIcon"]
      }) : v.downloadIcon,
      removeIcon: e["showUploadList.removeIcon"] ? /* @__PURE__ */ y.jsx(x, {
        slot: e["showUploadList.removeIcon"]
      }) : v.removeIcon,
      previewIcon: e["showUploadList.previewIcon"] ? /* @__PURE__ */ y.jsx(x, {
        slot: e["showUploadList.previewIcon"]
      }) : v.previewIcon,
      extra: e["showUploadList.extra"] ? /* @__PURE__ */ y.jsx(x, {
        slot: e["showUploadList.extra"]
      }) : v.extra
    } : s
  });
});
export {
  We as UploadDragger,
  We as default
};
